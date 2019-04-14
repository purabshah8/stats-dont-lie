from stats.models import *
import os
import django
import json
from util import get_datetime, update_auto_increments
from scraper import get_box_score_urls, get_box_score_info
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statsdontlie.settings")
django.setup()

# from stats.models import Team, Game, PlayerTeamSeason, Statline

basic_stat_names = ["mp", "fg", "fga", "fg_pct", "tp", "tpa", "tp_pct", "ft",
                    "fta", "ft_pct", "orb", "drb", "trb", "ast", "stl", "blk", 
                    "tov", "pf", "pts"]
advanced_stat_names = ["ts", "efg", "tpar", "ftr", "orb_pct", "drb_pct",
                       "trb_pct", "ast_pct", "stl_pct", "blk_pct", "tov_pct", 
                       "usg_rate", "ortg", "drtg"]

# player_stat_names = ["started", "plus_minus"]

def save_game(info):
    home = Team.find(info["home_team"])
    away = Team.find(info["away_team"])
    
    game_time = get_datetime(info["tipoff"])
    game_info = {
        "home_id": home.id,
        "away_id": away.id,
        "tipoff": game_time,
        "attendance": info["attendance"],
        "duration": info["duration"]
    }

    date = str(game_time.year) + str(game_time.month).zfill(2) + \
        str(game_time.day).zfill(2)
    game_info["id"] = date + away.abbreviation + home.abbreviation

    home_score = sum(info["scoring"]["home"])
    away_score = sum(info["scoring"]["away"])
    game_info["away_score"] = away_score
    game_info["home_score"] = home_score
    game_info["winner_id"] = game_info["home_id"] if home_score > away_score else game_info["away_id"]

    officials = info["officials"]
    ref_keys = ["ref_one", "ref_two", "ref_three"]
    for i, ref_name in enumerate(officials):
        person = Person.find(ref_name)
        game_info[ref_keys[i]] = person.referee
    
    if Game.objects.filter(**game_info).exists():
        game = Game.objects.get(**game_info)
        return game
    game = Game(**game_info)
    game.save()

    home_quarters = info["scorin`g"]["home"]
    away_quarters = info["scoring"]["away"]
    quarters = []
    for i, home_score in enumerate(home_quarters):
        quarter = {
            "game_id": game.id,
            "number": i+1,
            "home_score": home_score,
            "away_score": away_quarters[i]
        }
        quarter = GamePeriod(**quarter)
        quarter.save()
        quarters.append(quarter)

    year = game_time.year if game_time.month < 7 else game_time.year + 1
    teams = [home, away]
    team_loc = "home"

    for team in teams:
        team_season = team.get_season(year)
        team_stats = info[team_loc + "_stats"]
        team_players = team_stats.keys()
        invalid_keys = ["Team Totals", "inactive"]
        team_players = [player for player in team_players if bool(team_stats[player]) and player not in invalid_keys]
        for name in team_players:
            print(f"{name}")
            person = Person.find(name)
            if not PlayerTeamSeason.objects.filter(player_id=person.id, team_season_id=team_season.id).exists():
                team_membership = PlayerTeamSeason(
                    player_id=person.id, team_season_id=team_season.id)
                team_membership.save()
            
            player_stats = team_stats[name]
            # breakpoint()
            basic_statline = { stat:player_stats[stat] for stat in basic_stat_names }
            basic_statline["game_id"] = game.id
            basic_statline["team_id"] = team.id
            basic_statline = Statline(**basic_statline)
            basic_statline.save()

            # basic_stats = info[team_loc + "_stats"]["basic"][name]
            # started = basic_stats.pop()
            # plus_minus = basic_stats.pop()
            # statline = dict(zip(basic_stat_names, basic_stats))
            # breakpoint()
            player_statline = {
                "id": basic_statline,
                "player_id": person.id,
                "started": player_stats["started"],
                "plus_minus": player_stats["plus_minus"],
            }
            player_statline = PlayerStatline(**player_statline)
            player_statline.save()

            # breakpoint()
            advanced_statline = { stat:player_stats[stat] for stat in advanced_stat_names }
            # advanced_stats = info[team + "_stats"]["advanced"][name]
            # statline = dict(zip(advanced_stat_names, advanced_stats))
            # statline.pop("mp")
            
            advanced_statline["id"] = basic_statline
            advanced_statline = AdvancedStatline(**advanced_statline)
            advanced_statline.save()
        team_loc = "away"

    # print(f"""Created the follwing objects: 
    #         {game}, {basic_statline}, {player_statline}, 
    #         {advanced_statline}, {quarters}""")
    return game

def load_and_save_games(season):
    nba_months = ["october", "november", "december", "january", "february", "march", "april", "may", "june"]
    for month in nba_months:
        try:
            with open(f"data/seasons/{season}/{month}.json") as file:
                game_data = json.load(file)
                for game in game_data:
                    game = save_game(game)
                    print(f"Saved {game.id} to database.")
        except FileNotFoundError:
            pass
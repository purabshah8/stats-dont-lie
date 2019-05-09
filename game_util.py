import os
import django
import json
from stats.models import *
from util import *
from scraper import get_box_score_urls, get_box_score_info
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statsdontlie.settings")
django.setup()

def save_game(info):
    home = Team.find(info["home_team"])
    away = Team.find(info["away_team"])
    
    game_time = get_datetime(info["tipoff"])
    year = game_time.year if game_time.month < 7 else game_time.year + 1
    game_info = {
        "home_id": home.id,
        "away_id": away.id,
        "tipoff": game_time,
        "attendance": info["attendance"],
    }
    if "duration" in info:        
        game_info["duration"] = info["duration"]

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
        if i >= 3:
            break
        referees = Referee.find(ref_name)
        if len(referees) == 1:
            referee = referees[0]
        else:
            active_refs = []
            for ref in referees:
                if ref.is_active(year):
                    active_refs.append(ref)
            if len(active_refs) == 1:
                referee = active_refs[0]
            else:
                breakpoint()
                
        game_info[ref_keys[i]] = referee
    
    if Game.objects.filter(**game_info).exists():
        game = Game.objects.get(**game_info)
    else:
        game = Game(**game_info)
        game.save()

    home_quarters = info["scoring"]["home"]
    away_quarters = info["scoring"]["away"]
    quarters = []
    for i, home_score in enumerate(home_quarters):
        quarter = {
            "game_id": game.id,
            "number": i+1,
            "home_score": home_score,
            "away_score": away_quarters[i]
        }
        if GamePeriod.objects.filter(**quarter).exists():
            quarter = GamePeriod.objects.get(**quarter)
        else:
            quarter = GamePeriod(**quarter)
            quarter.save()
        quarters.append(quarter)

    teams = [home, away]
    team_loc = "home"

    for team in teams:
        team_season = team.get_season(year)
        team_stats = info[team_loc + "_stats"]
        team_players = team_stats.keys()
        invalid_keys = ["Team Totals", "inactive"]
        team_players = [player for player in team_players if bool(team_stats[player]) and player not in invalid_keys]
        for name in team_players:
            person = Person.find(name, year)
            if person is None:
                print("ERROR: Person not found")
                pass # add logic for multiple objects returned
                
            pts_info = { "player_id": person.id, "team_season_id": team_season.id }
            if not PlayerTeamSeason.objects.filter(**pts_info).exists():
                team_membership = PlayerTeamSeason(**pts_info)
                team_membership.save()
            
            player_stats = team_stats[name]
            basic_statline = { stat:player_stats[stat] for stat in BASIC_STAT_NAMES }
            basic_statline["game_id"] = game.id
            basic_statline["team_id"] = team.id
            if Statline.objects.filter(**basic_statline).exists():
                basic_statline = Statline.objects.get(**basic_statline)
            else:
                basic_statline = Statline(**basic_statline)
                basic_statline.save()

            player_statline = {
                "id": basic_statline,
                "player_id": person.id,
                "started": player_stats["started"],
                "plus_minus": player_stats["plus_minus"],
            }
            if PlayerStatline.objects.filter(**player_statline).exists():
                player_statline = PlayerStatline.objects.get(**player_statline)
            else:
                # breakpoint()
                player_statline = PlayerStatline(**player_statline)
                player_statline.save()

            advanced_statline = { stat:player_stats[stat] for stat in ADVANCED_STAT_NAMES }   
            advanced_statline["id"] = basic_statline
            
            if AdvancedStatline.objects.filter(**advanced_statline).exists():
                advanced_statline = AdvancedStatline.objects.get(**advanced_statline)
            else:
                advanced_statline = AdvancedStatline(**advanced_statline)
                advanced_statline.save()
        
        # save team totals (basic & advanced)
        basic_team_statline = {stat:team_stats["Team Totals"][stat] for stat in BASIC_STAT_NAMES}
        basic_team_statline["game_id"] = game.id
        basic_team_statline["team_id"] = team.id

        if Statline.objects.filter(**basic_team_statline).exists():
                basic_team_statline = Statline.objects.get(**basic_team_statline)
        else:
            basic_team_statline = Statline(**basic_team_statline)
            basic_team_statline.save()
        advanced_team_statline = {stat:team_stats["Team Totals"][stat] for stat in ADVANCED_STAT_NAMES}
        advanced_team_statline["id"] = basic_team_statline
        if AdvancedStatline.objects.filter(**advanced_team_statline).exists():
                advanced_team_statline = AdvancedStatline.objects.get(**advanced_team_statline)
        else:
            advanced_team_statline = AdvancedStatline(**advanced_team_statline)
            advanced_team_statline.save()
        team_loc = "away"

    return game

def load_and_save_games(season, nba_months=NBA_MONTHS):
    for month in nba_months:
        try:
            with open(f"data/seasons/{season}/{month}.json") as file:
                game_data = json.load(file)
                for game in game_data:
                    game = save_game(game)
                    print(f"Saved {game.id} to database.")
        except FileNotFoundError:
            pass


def delete_all_games():
    games = Game.objects.all()
    stats = Statline.objects.all()
    player_stats = PlayerStatline.objects.all()
    adv_stats = AdvancedStatline.objects.all()
    to_delete = [player_stats, adv_stats, stats, games]
    for class_objs in to_delete:
        for obj in class_objs:
            obj.delete()


# The basic building blocks of the Offensive Rating calculation are Individual Total Possessions and Individual Points Produced. The formula for Total Possessions is broken down into four components: Scoring Possessions, Missed FG Possessions, Missed FT Possessions, and Turnovers.

# The Scoring Possessions formula is by far the most complex:

# ScPoss = (FG_Part + AST_Part + FT_Part) * (1 - (Team_ORB / Team_Scoring_Poss) * Team_ORB_Weight * Team_Play%) + ORB_Part
# where:

# FG_Part = FGM * (1 - 0.5 * ((PTS - FTM) / (2 * FGA)) * qAST)
# qAST = ((MP / (Team_MP / 5)) * (1.14 * ((Team_AST - AST) / Team_FGM))) + ((((Team_AST / Team_MP) * MP * 5 - AST) / ((Team_FGM / Team_MP) * MP * 5 - FGM)) * (1 - (MP / (Team_MP / 5))))
# AST_Part = 0.5 * (((Team_PTS - Team_FTM) - (PTS - FTM)) / (2 * (Team_FGA - FGA))) * AST
# FT_Part = (1-(1-(FTM/FTA))^2)*0.4*FTA
# Team_Scoring_Poss = Team_FGM + (1 - (1 - (Team_FTM / Team_FTA))^2) * Team_FTA * 0.4
# Team_ORB_Weight = ((1 - Team_ORB%) * Team_Play%) / ((1 - Team_ORB%) * Team_Play% + Team_ORB% * (1 - Team_Play%))
# Team_ORB% = Team_ORB / (Team_ORB + (Opponent_TRB - Opponent_ORB))
# Team_Play% = Team_Scoring_Poss / (Team_FGA + Team_FTA * 0.4 + Team_TOV)
# ORB_Part = ORB * Team_ORB_Weight * Team_Play%
# Missed FG and Missed FT Possessions are calculated as follows:

# FGxPoss = (FGA - FGM) * (1 - 1.07 * Team_ORB%)
# FTxPoss = ((1 - (FTM / FTA))^2) * 0.4 * FTA
# Total Possessions are then computed like so:

# TotPoss = ScPoss + FGxPoss + FTxPoss + TOV


def calc_team_poss(info):
    # team info: fga, fta, orb, fga, fg, tov, drb
    # opp team info: drb, fga, fta, orb, fg, tov
    0.5 * ((info["fga"] + 0.4 * info["fta"] - 1.07 * (info["orb"] / (info["orb"] + info["opp_drb"])) * (info["fga"] - info["fg"]) + info["tov"]) + (info["opp_fga"] + 0.4 * info["opp_fta"] - 1.07 * (info["opp_orb"] / (info["opp_orb"] + info["drb"])) * (info["opp_fga"] - info["opp_fg"]) + info["opp_tov"]))


def calc_player_poss(info):
    # player info: mp, ast, fg, pts, ft, fga, fta, tov
    # team info: mp, ast, fg, pts, ft, fga, fta, orb, tov
    # opp team info: trb, orb
    qAST_0 = ((info["mp"] / (info["team_mp"] / 5)) * (1.14 * ((info["team_ast"] - info["ast"]) / info["team_fg"])))
    qAST_1 = (((info["team_ast"] / info["team_mp"]) * info["mp"] * 5 - info["ast"]) / ((info["team_fg"] / info["team_mp"]) * info["mp"] * 5 - info["fg"]))
    qAST = qAST_0 + (qAST_1 * (1 - (info["mp"] / (info["team_mp"] / 5))))
    fg_part = info["fg"] * (1 - 0.5 * ((info["pts"] - info["ft"]) / (2 * info["fga"])) * qAST)
    ast_part = 0.5 * (((info["team_pts"] - info["team_ft"]) - (info["pts"]-info["ft"])) / (2 * (info["team_fga"]-info["fga"]))) * info["ast"]
    ft_part = (1-(1-(info["ft"]/info["fta"])) ** 2) * 0.4 * info["fta"]
    team_scoring_poss = info["team_fg"] + (1 - (1-(info["team_ft"]/info["team_fta"])) ** 2) * info["team_fta"] * 0.4
    team_orb_pct = info["team_orb"] / (info["team_orb"] + (info["opp_trb"]-info["opp_orb"]))
    team_play_pct = team_scoring_poss / (info["team_fga"]+info["team_fta"]*0.4+info["team_tov"])
    team_orb_weight = ((1 - team_orb_pct) * team_play_pct) / ((1 - team_orb_pct) * team_play_pct + team_orb_pct * (1 - team_play_pct))
    orb_part = info["orb"] * team_orb_weight * team_play_pct
    sc_poss = (fg_part + ast_part + ft_part) * (1 - (info["team_orb"] / team_scoring_poss) * team_orb_weight * team_play_pct) + orb_part
    
    fg_poss = (info["fga"] - info["fg"]) * (1 - 1.07 * team_orb_pct)
    ft_poss = ((1 - (info["ft"]/info["fta"])) ** 2) * 0.4 * info["fta"]
    return sc_poss + fg_poss + ft_poss + info["tov"]
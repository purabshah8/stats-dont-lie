import os, django, json
from util import get_datetime, update_auto_increments
from scraper import get_box_score_urls, get_box_score_info
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statsdontlie.settings")
django.setup()

from stats.models import *
# from stats.models import Team, Game, PlayerTeamSeason, Statline

basic_stat_names = ['mp', 'fg', 'fga', 'fg_pct', 'tp', 'tpa', 'tp_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts']
advanced_stat_names = ['mp', 'ts', 'efg', 'tpar', 'ftr', 'orb_pct', 'drb_pct', 'trb_pct', 'ast_pct', 'stl_pct', 'blk_pct', 'tov_pct', 'usg_rate', 'ortg', 'drtg']

def save_game(info):
    home = Team.find(info['home_team'])
    away = Team.find(info['away_team'])

    game_info = {}
    game_info['home_id'] = home.id
    game_info['away_id'] = away.id
    
    date = str(info['tipoff'].year) + str(info['tipoff'].month).zfill(2) + str(info['tipoff'].day).zfill(2)
    game_info['id'] = date + away.abbreviation + home.abbreviation
    
    home_score = sum(info['scoring']['home'])
    away_score = sum(info['scoring']['away'])
    game_info['away_score'] = away_score
    game_info['home_score'] = home_score
    game_info['winner_id'] = game_info['home_id'] if home_score > away_score else game_info['away_id']
    
    game_info['tipoff'] = info['tipoff']
    game_info['attendance'] = info['attendance']
    game_info['duration'] = info['duration']
    
    officials = info['officials']
    ref_keys = ['ref_one', 'ref_two', 'ref_three']
    for i,ref_name in enumerate(officials):
        person = Person.find(ref_name)
        game_info[ref_keys[i]] = person.id
    game = Game(**game_info)
    game.save()

    home_quarters = info['scoring']['home']
    away_quarters = info['scoring']['away']
    for i,q in enumerate(home_quarters):
        quarter = { 'game_id': game.id, 'number': i+1, 'home_score': q, 'away_score': away_quarters[i] }
        quarter = GamePeriod(**quarter)
    game_time = info['tipoff']
    year = game_time.year if game_time.month < 7 else game_time.year + 1
    teams = [home, away]
    team_loc = 'home'

    for team in teams:
        team_season = team.get_season(year)
        team_players = info[team_loc + '_stats']['basic'].keys()
        team_loc = 'away'
        team_players = [player for player in team_players if player != 'Team Totals']
        for name in team_players:
            person = Person.find(name)
            if PlayerTeamSeason.objects.filter(player_id=person.id, team_season_id=team_season.id).exists():
                team_membership = PlayerTeamSeason.objects.get(player_id=person.id, team_season_id=team_season.id)
            else:
                team_membership = PlayerTeamSeason(player_id=person.id, team_season_id=team_season.id)
                team_membership.save()
            
            basic_stats = info[team + '_stats']['basic'][name]
            statline = dict(zip(basic_stat_names, basic_stats[:-1]))
            plus_minus = statline.pop('plus_minus')
            statline['game_id'] = game.id
            statline['team_id'] = team.id
            basic_statline = Statline(**statline)
            basic_statline.save()
            
            statline = { 'plus_minus' : basic_stats[-1] }
            statline['player_id'] = person.id
            statline['started'] = False # to change
            statline['id'] = basic_statline.id
            player_statline = PlayerStatline(**statline)
            player_statline.save()

            advanced_stats = info[team + '_stats']['advanced'][name]
            statline = dict(zip(advanced_stat_names, advanced_stats))
            statline['id'] = basic_statline.id
            statline.pop('mp')
            advanced_statline = AdvancedStatline(**statline)
            advanced_statline.save()
    print("Created the follwing objects: {Game,}")

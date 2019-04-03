import os, django, json
from util import get_datetime, update_auto_increments
from scraper import get_box_score_urls, get_box_score_info
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statsdontlie.settings")
django.setup()

from stats.models import *
# from stats.models import Team, 

def save_game(info):
    home_id = Team.find(info['home_team']).id
    away_id = Team.find(info['away_team']).id
    
    game = {}
    game['home_id'] = home_id
    game['away_id'] = away_id
    date = str(info['tipoff'].year) + str(info['tipoff'].month).zfill(2) + str(info['tipoff'].day).zfill(2)
    game['id'] = date + away_team.abbreviation + home_team.abbreviation
    game['away_score'] = sum(info['scoring']['away'])
    game['home_score'] = sum(info['scoring']['home'])
    game['winner_id'] = game['home_id'] if home_score > away_score else game['away_id']
    game['tipoff'] = info['tipoff']
    game['attendance'] = info['attendance']
    game['duration'] = info['duration']
    g = Game(game)
    g.save()

    info['away_stats']

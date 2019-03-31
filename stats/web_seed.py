import os, sys, django, psycopg2
from django.utils.six import StringIO
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statsdontlie.settings")
django.setup()

from stats.web_scraper import *
from stats.models import *

def update_auto_increments():
    output = StringIO()
    django.core.management.call_command('sqlsequencereset', 'stats', stdout=output, no_color=True)
    connection = None
    try:
        connection = psycopg2.connect("dbname=nba user=purab password=godricshallows")
        cursor = connection.cursor()
        cursor.execute(output.getvalue())
        cursor.close()
        connection.commit()
    except psycopg2.DatabaseError as e:
        if connection:
            connection.rollback()
            print("rolling back...")
        print('Error %s' % e)
        sys.exit(1)
    finally:
        if connection:
            connection.close()

    # print(type(output.getvalue()))
    # return output.getvalue()

states = ['Alabama','Alaska','American Samoa','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Federated States of Micronesia','Florida','Georgia','Guam','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Marshall Islands','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Northern Mariana Islands','Ohio','Oklahoma','Oregon','Palau','Pennsylvania','Puerto Rico','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','U.S. Virgin Islands','Virginia','Washington','West Virginia','Wisconsin','Wyoming']

def add_player(player, person):
    
    # add location if it does not exist
    city, state = person.pop('birth_place').split(", ")
    if state not in states:
        country = state
        state = None
    else:
        country = 'USA'
    location = { 'city': city, 'country': country, 'precision': 'city'}
    if state:
        location['state'] = state
    player_location = Location.objects.filter(precision="city", country=location['country'], city=location['city'])
    if len(player_location) == 0:
        print('Location not found!')
        player_location = Location(**location)
        player_location.save()
    else:
        player_location = player_location[0]
    
    # save person to database
    person['birthplace_id'] = player_location.id
    person = Person(**person)
    person.save()

    # save player to database
    player['id'] = person.id
    league_id = 1
    if player['aba'] == True:
        league_id = 2
    player['rookie_season_id'] = Season.objects.get(year=player.pop('rookie_season'), league_id=league_id).id
    if player['aba'] == True and player['final_season'] > 1976:
        league_id = 1
    player['final_season_id'] = Season.objects.get(year=player.pop('final_season'), league_id=league_id).id
    if player['aba'] == True:
        player.pop('aba')
    positions = player.pop('positions')
    player = Player(**player)
    player.save()

    # save positions to database
    for position in positions:
        position_id = Position.objects.get(abbreviation=position)
        player_position = PlayerPosition(player_id=player.id, position_id=position_id)
        player_position.save()
        
# if __name__ == "__main__":
#     player_urls = get_player_urls()
#     for url in player_urls:
#         player, person = get_player_info(url)
#         add_player(player, person)
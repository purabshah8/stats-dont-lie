from web_scraper import *
from models import *

states = ['Alabama','Alaska','American Samoa','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Federated States of Micronesia','Florida','Georgia','Guam','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Marshall Islands','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Northern Mariana Islands','Ohio','Oklahoma','Oregon','Palau','Pennsylvania','Puerto Rico','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','U.S. Virgin Islands','Virginia','Washington','West Virginia','Wisconsin','Wyoming']

def add_player(player, person):
    city, state = person.pop('birth_place').split(", ")
    if state not in states:
        country = state
        state = None
    else:
        country = 'USA'
    location = { 'city': city, 'country': country}
    if state:
        location['state'] = state
    l = Location(**location)
    l.save()
    person['birthplace_id'] = l.id
    person = Person(**person)
    person.save()
    player['rookie_season_id'] = Season.objects.find(year=player.pop('rookie_season'))
    player['final_season_id'] = Season.objects.find(year=player.pop('final_season'))
    player['id'] = person.id
    player = Player(**player)
    player.save()

player_urls = get_player_urls()
for url in player_urls:
    add_player(get_player_info(url))
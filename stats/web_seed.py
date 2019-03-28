from web_scraper import get_box_score_info, get_box_score_urls, get_player_info, get_player_urls
from models import Person, Team, Player, Position, PlayerPosition, League, Season, Location

states = ['Alabama','Alaska','American Samoa','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Federated States of Micronesia','Florida','Georgia','Guam','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Marshall Islands','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Northern Mariana Islands','Ohio','Oklahoma','Oregon','Palau','Pennsylvania','Puerto Rico','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','U.S. Virgin Islands','Virginia','Washington','West Virginia','Wisconsin','Wyoming']


def add_player(person, player):
    city, state = person['birth_place'].pop().split(", ")
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

player_urls = get_player_urls()
for url in player_urls:
    person, player = get_player_info(url)
    
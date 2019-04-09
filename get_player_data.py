from stats.models import Location, Person, Player, Position, Season, PlayerPosition
import os
import django
import json
from util import get_datetime, update_auto_increments, states
from scraper import *
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statsdontlie.settings")
django.setup()

def save_person(person):
    if "birth_place" in person:
        # add location if it does not exist
        locs = person.pop("birth_place").split(", ")
        if len(locs) > 1:
            city, state = locs
            if state not in states:
                country = state
                state = None
            else:
                country = "USA"
            location = {"city": city, "country": country, "precision": "city"}
            if state:
                location["state"] = state
        else:
            location = {"country": locs[0], "precision": "country"}
        if Location.objects.filter(**location).exists():
            player_location = Location.objects.filter(**location)[0]
        else:
            player_location = Location(**location)
            player_location.save()
        person["birthplace_id"] = player_location.id
    
    # save person to database
    if "dob" in person:
        person["dob"] = get_datetime(person["dob"])
    if Person.objects.filter(**person).exists():
        person = Person.objects.filter(**person)[0]
    else:
        person = Person(**person)
        person.save()
    return person


def save_player(player, person):
    # save player to database
    player["id"] = person
    league_id = 1
    if "aba" not in player:
        player["aba"] = False
    if "rookie_season" not in player:
        player["rookie_season"] = 1947
    if player["aba"] == True:
        league_id = 2
    if not Season.objects.filter(year=player["rookie_season"], league_id=league_id).exists():
        league_id = 1
    player["rookie_season_id"] = Season.objects.get(
        year=player.pop("rookie_season"), league_id=league_id).id

    if "final_season" in player:
        if player["aba"] == True and player["final_season"] > 1976:
            league_id = 1
        if not Season.objects.filter(year=player["final_season"], league_id=league_id).exists():
            league_id = 2
        player["final_season_id"] = Season.objects.get(
            year=player.pop("final_season"), league_id=league_id).id
    player.pop("aba")
    positions = player.pop("positions")
    if Player.objects.filter(**player).exists():
        player = Player.objects.filter(**player)[0]
    else:
        player = Player(**player)
        player.save()
    return player

    # save positions to database
    for position in positions:
        position_id = Position.objects.get(abbreviation=position).id
        if not PlayerPosition.objects.filter(player_id=person.id, position_id=position_id):
            player_position = PlayerPosition(
                player_id=person.id, position_id=position_id)
            player_position.save()


def save_players(letter):
    info = []
    urls = get_player_urls(letter)
    print(f"Retrieved urls for players with last name beginning with {letter}")
    for url in urls:
        short_url = url.split("/")[-1].split(".html")[0]
        print(f"Fetching {short_url}...")
        info.append(get_player_info(url))
        print("Done!")
    with open(f"data/players/{letter}.json", "w") as file:
        json.dump(info, file, indent=4, sort_keys=True)


def load_players(letter, repeat=False):
    try:
        with open(f"data/players/{letter}.json") as file:
            player_data = json.load(file)
            for datum in player_data:
                person = save_person(datum["person"])
                player = save_player(datum["player"], person)
                # add_player(datum["player"], datum["person"])
                name = person["preferred_name"] + " " + person["last_name"]
                print(f"Saved {name} to database.")

    except FileNotFoundError:
        if repeat:
            print(
                f"Error! File not found. I tried to scrape the data again and save it to ./data/players/{letter}.json, but was unsuccessful.")
        else:
            print("File not found. Attempting to scrape web and create json file...")
            save_players(letter)
            load_players(letter, True)


def delete_player(info):
    try:
        person = Person.objects.get(**info)
        player = person.player
        name = person.preferred_name + " " + person.last_name
        player_positions = PlayerPosition.objects.filter(player=person.id)
        for pos in player_positions:
            pos.delete()
        player.delete()
        person.delete()
        print(f"{name} removed from database.")
    except ObjectDoesNotExist:
        print("No matching player in database.")


def save_ref(person, referee):
    referee["id"] = person
    
    first_season = Season.objects.get(year=referee["rookie_season"], league_id=1)
    referee["rookie_season"] = first_season
    
    if referee["final_season"]:
        last_season = Season.objects.get(year=referee["final_season"], league_id=1)
        referee["final_season"] = last_season

    referee = Referee(**referee)
    referee.save()


def load_refs():
    urls = get_ref_urls()
    info = []
    for url in urls:
        info.append(get_ref_info(url))
        short_url = url.split("/")[-1].split(".html")[0]
        print(f"added ref @ {short_url}")

    with open(f"data/referees.json", "w") as file:
        json.dump(info, file, indent=4, sort_keys=True)

if __name__ == "__main__":
    update_auto_increments()
    letters = "abcdefghijklmnopqrstuvwyz"
    for letter in letters:
        load_players(letter)

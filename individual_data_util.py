from stats.models import Location, Person, Player, Position, Season, PlayerPosition, Referee
import os
import django
import json
from util import get_datetime, update_auto_increments, states
from scraper import scrape_players, scrape_refs
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statsdontlie.settings")
django.setup()

def save_person_to_db(person):
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

    if "dob" in person:
        person["dob"] = get_datetime(person["dob"])
    
    already_exists = False
    if Person.objects.filter(**person).exists():
        person = Person.objects.filter(**person)[0]
        already_exists = True
    else:
        person = Person(**person)
        person.save()
    print_str = "exists in" if already_exists else "saved to"
    print(f"{person.get_name()} {print_str} database.")
    
    return person


def save_player_to_db(player, person):
    person = save_person_to_db(person)
    
    player["id"] = person
    league_id = 1
    
    ### TO REMOVE - check if key abay is not in player
    if "aba" not in player:
        print(f"Key 'aba' not found in Player {person.get_name()}")
        player["aba"] = False

    if "rookie_season" not in player:
        player["rookie_season"] = 1947 # some players played in the debut season don't have that listed
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
    
    already_exists = False
    if Player.objects.filter(**player).exists():
        player = Player.objects.filter(**player)[0]
        already_exists = True
    else:
        player = Player(**player)
        player.save()
    print_str = "exists in" if already_exists else "saved to"
    print(f"Player {person.get_name()} {print_str} database.")
    

    # save positions to database
    already_saved = True
    for position in positions:
        position_id = Position.objects.get(abbreviation=position).id
        if not PlayerPosition.objects.filter(player_id=person.id, position_id=position_id):
            already_saved = False
            player_position = PlayerPosition(
                player_id=person.id, 
                position_id=position_id)
            player_position.save()
    if not already_saved:
        print(f"Positions for Player {person.get_name()} saved to database.")
    return player


def save_ref_to_db(person, referee):
    person = save_person_to_db(person)
    referee["id"] = person

    first_season = Season.objects.get(
        year=referee.pop("rookie_season"), 
        league_id=1)
    referee["rookie_season_id"] = first_season.id

    if referee["final_season"]:
        last_season = Season.objects.get(
            year=referee.pop("final_season"), 
            league_id=1)
        referee["final_season_id"] = last_season.id
    else:
        ## TODO: Remove "final_season": null, from all refs in "data/referees.json" 
        referee.pop("final_season")
    already_exists = False
    if Referee.objects.filter(**referee).exists():
        referee = Referee.objects.filter(**referee)[0]
        already_exists = True
    else:
        referee = Referee(**referee)
        referee.save()
    print_str = "exists in" if already_exists else "saved to"
    print(f"Referee {person.get_name()} {print_str} database.")

    return referee


def load_and_save_players(letter, repeat=False):
    try:
        with open(f"data/players/{letter}.json") as file:
            player_data = json.load(file)
            for datum in player_data:
                person = save_person_to_db(datum["person"])
                save_player_to_db(datum["player"], person)
                name = person["preferred_name"] + " " + person["last_name"]
                print(f"Saved {name} to database.")

    except FileNotFoundError:
        if repeat:
            print(
                f"Error! File not found. I tried to scrape the data again and save it to ./data/players/{letter}.json, but was unsuccessful.")
        else:
            print("File not found. Attempting to scrape web and create json file...")
            scrape_players(letter)
            load_and_save_players(letter, True)


def load_and_save_refs(repeat=False):
    try:
        with open('data/referees.json') as file:
            ref_data = json.load(file)
            for datum in ref_data:
                referee = save_ref_to_db(**datum)
    except FileNotFoundError:
        if repeat:
            print("Error! File not found. I tried to scrape the data again and save it to ./data/referees.json, but was unsuccessful.")
        else:
            print("File not found. Attempting to scrape web and create json file...")
            scrape_refs()
            load_and_save_refs(True)


def delete_person(info, category="person", delete_person=True):
    category = category.lower()
    try:
        person = Person.objects.get(**info)
        name = person.preferred_name + " " + person.last_name

        if category == "player":
            player = person.player
            player_positions = PlayerPosition.objects.filter(player=person.id)
            for pos in player_positions:
                pos.delete()
            player.delete()
            print(f"Player {name} removed from database.")
        elif category == "referee":
            referee = person.referee
            referee.delete()
            print(f"Referee {name} removed from database.")
        elif category == "team employee":
            pass

        if delete_person:
            person.delete()
            print(f"Person {name} removed from database.")

    except ObjectDoesNotExist:
        print("Couldn't find a match in the database with the given information.")


if __name__ == "__main__":
    update_auto_increments()
    letters = "abcdefghijklmnopqrstuvwyz"
    for letter in letters:
        load_and_save_players(letter)
    load_and_save_refs()

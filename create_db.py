import os, django
from create_tables import create_tables
from seed_data import tables, seed_data, insert
from util import update_auto_increments
from person_util import load_and_save_players, load_and_save_refs
from game_util import load_and_save_games

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statsdontlie.settings")
django.setup()

if __name__ == "__main__":
    create_tables()
    for i in range(len(seed_data)):
        insert(tables[i], seed_data[i])
    update_auto_increments()    
    letters = "abcdefghijklmnopqrstuvwyz"
    for letter in letters:
        load_and_save_players(letter)
    update_auto_increments()    
    load_and_save_refs()
    load_and_save_games(2019)
    update_auto_increments()
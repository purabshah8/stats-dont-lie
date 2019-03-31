import os, sys, django, psycopg2, json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statsdontlie.settings")
django.setup()

from stats.web_scraper import get_player_urls, get_player_info
from stats.web_seed import add_player

def save_players(letter):
    info = []
    urls = get_player_urls(letter)
    print(f"Retrieved urls for players with last name beginning with {letter}")
    for url in urls:
        print(f"Fetching {url.split('/')[-1].split('.html')[0]}...")
        info.append(get_player_info(url))
        print("Done!")
    with open(f"data/players/{letter}.json", "w") as file:
        json.dump(info, file, indent=4, sort_keys=True)


def load_players(letter, repeat=False):
    try:
        with open(f'data/players/{letter}.json') as file:
            player_data = json.load(file)
            for datum in player_data:
                add_player(datum['player'], datum['person'])
                print("Saved {0} {1} to database.")
        
    except FileNotFoundError:
        if repeat:
            print(f"Error! File not found. I tried to scrape the data again and save it to ./data/players/{letter}.json, but was unsuccessful.")
        else:
            print("File not found. Attempting to scrape web and create json file...")
            save_players(letter)
            load_players(letter, True)

if __name__ == '__main__':
    # letters = "abcdefghijklmnopqrstuvwyz"
    # for letter in letters:
        # load_players(letter)

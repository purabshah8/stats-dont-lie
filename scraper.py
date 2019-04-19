import csv
import re
import json

import pytz

import bs4
import requests
from util import get_datetime, NBA_MONTHS


def get_box_score_urls(season=2019, months=NBA_MONTHS):
    if season == 2019 and len(months) > 7:
        months.pop()
        months.pop()
    urls = []
    for month in months:
        response = requests.get(f"https://www.basketball-reference.com/leagues/NBA_{season}_games-{month}.html")
        if response.status_code == 200:
            scores_soup = bs4.BeautifulSoup(response.text, "html.parser")
            box_scores = scores_soup.find_all("a", string="Box Score")
            for score in box_scores:
                urls.append(score["href"])
        else:
            response.raise_for_status()
    return urls


def get_box_score_info(url):
    response = requests.get("https://www.basketball-reference.com" + url)
    if response.status_code == 200:
        box_soup = bs4.BeautifulSoup(response.text, "html.parser")
        info = {
            "home_stats": {},
            "away_stats": {},
        }
        stat_map = {
            "fg3": "tp",
            "fg3a": "tpa",
            "fg3_pct": "tp_pct",
            "ts_pct": "ts",
            "efg_pct": "efg",
            "fg3a_per_fga_pct": "tpar",
            "fta_per_fga_pct": "ftr",
            "usg_pct": "usg_rate",
            "off_rtg": "ortg",
            "def_rtg": "drtg"
        }

        teams = box_soup.find("h1").get_text().split(" at ")
        teams[1] = teams[1].split(" Box Score, ")[0]
        info["away_team"], info["home_team"] = teams

        tables = box_soup("tbody")
        footers = box_soup("tfoot")
        for i, table in enumerate(tables):
            
            box_type = "basic" if i % 2 == 0 else "advanced"
            team_stats = "away_stats" if i < 2 else "home_stats"
            team_data = info[team_stats]

            table = [
                row for row in table.children 
                if isinstance(row, bs4.element.Tag) 
                and len(row.select("a")) > 0
            ]
            for j, row in enumerate(table):
                stats = row.select("td")
                data_dict = {}
                if len(stats) > 1:
                    for stat in stats:
                        stat_name = stat_map[stat["data-stat"]] if stat["data-stat"] in stat_map else stat["data-stat"]
                        stat_val = stat.text if stat.text else "0.0"
                        stat_val = str_to_data(stat_val)
                        data_dict[stat_name] = stat_val

                    if box_type == "basic":
                        started = True if j < 5 else False
                        data_dict["started"] = started
              
                name = row.select("a")[0].text
                if name in team_data:
                    team_data[name].update(data_dict)
                else:
                    team_data[name] = data_dict
            footer = [
                row for row in footers[i].children 
                if isinstance(row, bs4.element.Tag)
            ]
            for row in footer:
                stats = row(class_="right")
                data_dict = {}
                for stat in stats:
                    stat_name = stat_map[stat["data-stat"]] if stat["data-stat"] in stat_map else stat["data-stat"]
                    stat_val = stat.text if stat.text else "0.0"
                    stat_val = str_to_data(stat_val)
                    data_dict[stat_name] = stat_val
                if box_type == "advanced":
                    data_dict["mp"] *= 3600
            
            if "Team Totals" in team_data:
                team_data["Team Totals"].update(data_dict)
            else:
                team_data["Team Totals"] = data_dict
            
            info[team_stats] = team_data

        scores = box_soup.find(id="all_line_score")
        score = [s for s in scores if isinstance(s, bs4.element.Comment)][0]
        score_soup = bs4.BeautifulSoup(score, "html.parser")
        all_quarters = score_soup("td")
        num_periods = int(len(all_quarters)/2 - 2)
        away_quarters = all_quarters[1:num_periods+1]
        away_quarters = [int(q.text) for q in away_quarters]
        home_quarters = all_quarters[num_periods+3:-1]
        home_quarters = [int(q.text) for q in home_quarters]
        info["scoring"] = {"away": away_quarters, "home": home_quarters}

        scorebox = box_soup.find(class_="scorebox_meta")
        info["tipoff"] = scorebox.div.get_text()
        info["location"] = scorebox.div.next_sibling.get_text().split(",")[0]

        misc_info = box_soup.find(text="Inactive:").parent.parent
        misc_info = misc_info.text.replace("\xa0", " ").split("\n")
        misc_info = [el for el in misc_info if el]
        # breakpoint()
        attendance_idx = -2
        if len(misc_info) < 5:
            attendance_idx = -1
        else:
            game_length = misc_info[-1].split(": ")[-1]
            game_length = game_length.split(":")
            info["duration"] = 60 * int(game_length[0]) + int(game_length[1])

        info["attendance"] = int(misc_info[attendance_idx].split(": ")[-1].replace(",", ""))
        info["officials"] = misc_info[2][11:].split(", ")

        inactives = misc_info[1].split("   ")
        info["away_stats"]["inactive"] = inactives[0][4:].split(", ")
        info["home_stats"]["inactive"] = inactives[1][4:].split(", ")

        

    else:
        response.raise_for_status()
    return info


def get_player_urls(letters="abcdefghijklmnopqrstuvwyz"):
    """Return a list of player urls whose last name begin with the characters in the input string. Default input is a string of all letters (execpt x)"""
    player_urls = []
    for letter in letters:
        response = requests.get(
            f"https://www.basketball-reference.com/players/{letter}/")
        if response.status_code == 200:
            player_names_soup = bs4.BeautifulSoup(response.text, "html.parser")
            player_tables = player_names_soup("tbody")
            for table in player_tables:
                for row in table.children:
                    if not isinstance(row, bs4.element.NavigableString):
                        player_name = row.select("a")
                        player_urls.append(player_name[0]["href"])
        else:
            response.raise_for_status()
    return player_urls


def get_player_info(url):
    """Fetch a player's information from bbref and return a dict of dicts containing personal and player information"""
    player_response = requests.get(
        "https://www.basketball-reference.com" + url)
    player_soup = bs4.BeautifulSoup(player_response.text, "html.parser")

    person = {}
    player = {}

    image_url = player_soup.find(attrs={"itemscope": "image"})
    if image_url is not None:
        player["image_url"] = image_url["src"]

    player_info = player_soup.find(
        attrs={"itemtype": "https://schema.org/Person"})
    name = player_info.find("h1").get_text().split(" ")
    player_info = player_info("p")
    person["preferred_name"] = name[0]
    if len(name) < 2:
        name.append("Hilario")
    last_name = name[1]

    raw_info = []
    for info in player_info:
        raw_info.append(info.get_text().replace("\n", " "))
    ignore = ["Pronunciation", "High School", "Hall of Fame", "Draft",
              "Experience", "Relatives", "Died", "Recruiting", "(born"]

    for info in raw_info:
        if any(string in info for string in ignore):
            continue
        # clean up info
        info = info.replace("\xa0", " ").split(" ")
        info_arr = [x for x in info if x]

        if last_name in info_arr:
            full_name = " ".join(info_arr).split("▪")[0].split(" ")
            last_name_idx = full_name.index(last_name)
            person["last_name"] = " ".join(full_name[last_name_idx:]).strip().strip(
                "I").strip().replace("Jr.", "").strip()
            person["middle_name"] = " ".join(
                full_name[1:last_name_idx]).strip()
            person["first_name"] = full_name[0]

            # players with 3 names (and James Michael McAdoo)
            special_names = ["Jo English", "Rod Hundley", "Carlos Navarro", "John Ramos",
                             "Ray Richardson", "Michael Ray McAdoo", "Vander Velden", "Rod Williams"]
            if person["last_name"] in special_names or re.search(r"^[vV][ao]n ", person["last_name"]):
                names = person["last_name"].split(" ")
                person["middle_name"] = " ".join(names[0:-1])
                person["preferred_name"] = person["preferred_name"] + \
                    " " + names[0]
                person["last_name"] = names[-1]

        if "Position:" in info_arr:
            positions = {
                "Point": "PG",
                "Shooting": "SG",
                "Small": "SF",
                "Power": "PF",
                "Center": "C",
                "Guard": "G",
                "Forward": "F"
            }
            player["shooting_hand"] = info_arr[-1]
            block_idx = info_arr.index("▪")
            position_string = " ".join(info_arr[1:block_idx])
            position_list = re.findall(
                r"[\w']+", " ".join(position_string.split("and")))
            player_positions = set()
            for pos in position_list:
                player_positions.add(positions[pos])
            player["positions"] = list(player_positions)

        if "kg" in " ".join(info_arr):
            player["weight"] = float(info_arr[-1].split("kg")[0])
            player["height"] = float(info_arr[-2].split("cm")[0][1:])

        if "Born:" in info_arr:
            birth_date = " ".join(info_arr[1:4])
            person["dob"] = birth_date
            if len(info_arr) > 4:
                in_idx = info_arr.index("in")
                person["birth_place"] = " ".join(info_arr[in_idx+1:-1])

        if "College:" in info_arr or "Colleges:" in info_arr:
            person["college"] = " ".join(info_arr[1:])

        if "Debut:" in info_arr:
            debut_info = " ".join(info_arr).split("&blacksquare")
            if len(debut_info) > 1:
                debut_years = [info.split(" ")[-1] for info in debut_info]
                if debut_years[0] < debut_years[1]:
                    debut_idx = 0
                else:
                    debut_idx = 1
                debut_info = debut_info[debut_idx].strip().split(" ")
                debut_date = get_datetime(debut_info[-1].split(":")[-1])
                player["aba"] = True
            else:
                debut_date = get_datetime(debut_info[-1].split(":")[-1])
                player["aba"] = False
            rookie_year = debut_date.year + 1
            if debut_date.month < 7:
                rookie_year -= 1
            player["rookie_season"] = rookie_year

    player_seasons = player_soup.find_all(
        attrs={"data-stat": "season", "scope": "row", "class": "left"})
    player_seasons = [season for season in player_seasons if season("a")]
    final_season = player_seasons[-1].get_text()
    final_season = int(final_season[0:2] + final_season[-2:])
    if final_season == 1900:
        final_season = 2000
    if final_season != 2019:
        player["final_season"] = final_season

    return {"player": player, "person": person}


def get_season_dates(year):
    """Return list of season start and playoff start dates for NBA season ending in year"""
    url = f"https://en.wikipedia.org/wiki/{year-1}-{year % 100}_NBA_season"
    if year % 100 < 10:
        url = f"https://en.wikipedia.org/wiki/{year-1}-0{year % 100}_NBA_season"
    response = requests.get(url)
    if response.status_code == 200:
        season_soup = bs4.BeautifulSoup(response.text, "html.parser")
        dates = season_soup("table", class_="infobox")[0].select("tbody tr")[3]
        date_string = None
        for i, d in enumerate(dates):
            if i != 0:
                date_string = d.get_text(separator="\n")
        date_list = date_string.split("\n")
        date_list = [date.replace("\xa0", " ").replace(
            " (Playoffs)", "").strip() for date in date_list]
        season_start = date_list[0].split(" – ")[0].strip()
        if year == 1999:
            season_start += " 1999"
        playoff_start = date_list[1].split("–")[0].strip()
        if playoff_start[-4:] != str(year):
            playoff_start += f" {year}"
        season_start = get_datetime(season_start)
        playoff_start = get_datetime(playoff_start)
    else:
        response.raise_for_status()
    return [season_start, playoff_start]


def get_season_info():
    with open("data/season_info.csv", mode="w") as file:
        writer = csv.writer(file, delimiter="|",
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for year in range(1947, 2020):
            i = year - 1946
            season_start, playoff_start = get_season_dates(year)
            season_info = [i, 1, year, season_start, playoff_start]
            writer.writerow(season_info)
        start_dates = ["October 13, 1967", "October 18, 1968", "October 17, 1969", "October 14, 1970",
                       "October 13, 1971", "October 12, 1972", "October 10, 1973", "October 18, 1974", "October 24, 1975"]
        playoff_dates = ["March 23, 1968", "April 5, 1969", "April 17, 1970", "April 1, 1971",
                         "March 31, 1972", "March 30, 1973", "March 29, 1974", "April 4, 1975", "April 8, 1976"]
        i += 1
        for year in range(1968, 1977):
            j = year - 1968
            season_info = [i, 2, year, get_datetime(
                start_dates[j]), get_datetime(playoff_dates[j])]
            writer.writerow(season_info)
            i += 1


def get_ref_urls():
    response = requests.get("https://www.basketball-reference.com/referees/")
    ref_soup = bs4.BeautifulSoup(response.text, "html.parser")
    links = ref_soup.find(id="all_referees")("a")
    links = [l["href"] for l in links if "referees"in l["href"]]
    return links


def get_ref_info(url):
    ref_response = requests.get("https://www.basketball-reference.com" + url)
    ref_soup = bs4.BeautifulSoup(ref_response.text, "html.parser")
    person = {}
    referee = {}

    ref_info = ref_soup.find(attrs={"itemtype": "https://schema.org/Person"})
    jersey_num = ref_info.find("svg")
    if jersey_num:
        referee["jersey_number"] = int(jersey_num.text.replace("\n", ""))
    name = ref_info.find("h1").next_sibling.next_sibling.get_text()
    name = name.replace(" Sr.", "").replace(" Jr.", "")
    names = name.split(" ")
    person["preferred_name"] = names[0]
    person["first_name"] = names[0]
    person["last_name"] = names[-1]
    if len(names) > 2:
        person["middle_name"] = " ".join(names[1:-1])

    # for Sir Allen Conner
    if person["preferred_name"] == "Sir":
        person["preferred_name"] == "Sir " + person["middle_name"]
        person["first_name"] = person["middle_name"]
        person["middle_name"] = ""

    def has_correct_classes(css_class):
        return css_class == "left " or css_class == "left"

    seasons = ref_soup(class_=has_correct_classes, attrs={"data-stat": "season"})
    if not seasons:
        season_comment = ref_soup.find(id="all_raw_p").contents[-2]
        season_soup = bs4.BeautifulSoup(season_comment, 'html.parser')
        seasons = season_soup(class_=has_correct_classes, attrs={"data-stat": "season"})

    def extract_year(season):
        year = int(season.text[:2] + season.text[-2:])
        if year == 1900:
            year = 2000
        elif year == 2019:
            return None
        return year

    referee["rookie_season"] = extract_year(seasons[0])
    referee["final_season"] = extract_year(seasons[-2])
    ref_info = ref_info("p")
    ref_info = [i.get_text() for i in ref_info]
    raw_info = []
    for info in ref_info:
        contents = info.split("\n")
        contents = [c for c in contents if c]
        raw_info += contents

    for info in raw_info:
        info = info.replace("\xa0", " ").split(" ")
        info_arr = [x for x in info if x]
        if "Born:" in info_arr:
            birth_date = " ".join(info_arr[1:4])
            person["dob"] = birth_date
            if len(info_arr) > 4:
                in_idx = info_arr.index("in")
                person["birth_place"] = " ".join(info_arr[in_idx+1:])

        if "College:" in info_arr or "Colleges:" in info_arr:
            person["college"] = " ".join(info_arr[1:])

    return {"person": person, "referee": referee}


def scrape_players(letter):
    info = []
    urls = get_player_urls(letter)
    print(f"Retrieved urls for players with last name beginning with {letter}.")
    for url in urls:
        short_url = url.split("/")[-1].split(".html")[0]
        print(f"Fetching {short_url}...")
        info.append(get_player_info(url))
        print("Done!")
    with open(f"data/players/{letter}.json", "w") as file:
        json.dump(info, file, indent=4, sort_keys=True)

def scrape_refs():
    urls = get_ref_urls()
    info = []
    for url in urls:
        info.append(get_ref_info(url))
        short_url = url.split("/")[-1].split(".html")[0]
        print(f"added ref @ {short_url}")

    with open("data/referees.json", "w") as file:
        json.dump(info, file, indent=4, sort_keys=True)


def scrape_games(season, months=NBA_MONTHS):
    for month in months:
        urls = get_box_score_urls(season, [month])
        games = []
        for url in urls:
            game = get_box_score_info(url)
            games.append(game)
            print_str = game["away_team"] + " @ " + game["home_team"] + " " + str(game["tipoff"])
            print(f"Downloaded {print_str} ")
        
        with open(f"data/seasons/{season}/{month}.json", "w") as file:
            json.dump(games, file, indent=4, sort_keys=True)


def str_to_data(el):
    if "." in el:
        return float(el)
    elif ":" in el:
        stat = el.split(":")
        return 60 * int(stat[0]) + int(stat[1])
    else:
        return int(el)
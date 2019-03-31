import requests, bs4, re, pytz
from dateutil.parser import parse

def get_box_score_urls(season="2019"):
    months = ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may', 'june']
    if season == 2019:
        months.pop()
        months.pop()
    urls = []
    for month in months:
        response = requests.get(f"https://www.basketball-reference.com/leagues/NBA_{season}_games-{month}.html")
        if response.status_code == 200:
            scores_soup = bs4.BeautifulSoup(response.text, 'html.parser')
            box_scores = scores_soup.find_all('a', string="Box Score")
            for score in box_scores:
                urls.append(score['href'])
        else:
            response.raise_for_status()
    return urls

def get_box_score_info(url):
    response = requests.get("https://www.basketball-reference.com" + url)
    if response.status_code == 200:
        box_soup = bs4.BeautifulSoup(response.text, 'html.parser')
        tables = box_soup("tbody")
        box_basic = []
        box_advanced = []
        for (i, table) in enumerate(tables):
            team_data = []
            for row in table.children:
                if not isinstance(row, bs4.element.NavigableString) and len(row.select("a")) > 0:
                    data_row = []
                    data_row.append(row.select("a")[0].text)
                    stats = row.select("td")
                    for stat in stats:
                        if ":" in stat.text:
                            stat = stat.text.split(":")
                            stat = int(stat[0])*60 + int(stat[1])
                            data_row.append(stat)
                        elif "." in stat.text:
                            data_row.append(float(stat.text))
                        elif stat.text == "":
                            data_row.append(0)
                        elif stat.text == "Did Not Play" or stat.text == "Did Not Dress":
                            pass
                        else:
                            data_row.append(int(stat.text))
                    if len(data_row) > 1:
                        team_data.append(data_row)
            if i % 2 == 0:
                box_basic += team_data
            else:
                box_advanced += team_data
    else:
        response.raise_for_status()
    return [box_basic, box_advanced]

def get_player_urls(letters = "abcdefghijklmnopqrstuvwyz"):
    """Return a list of player urls whose last name begin with the characters in the input string. Default input is a string of all letters (execpt x)"""
    player_urls = []
    for letter in letters:
        response = requests.get(f"https://www.basketball-reference.com/players/{letter}/")
        if response.status_code == 200:
            player_names_soup = bs4.BeautifulSoup(response.text, 'html.parser')
            player_tables = player_names_soup("tbody")
            for table in player_tables:
                for row in table.children:
                    if not isinstance(row, bs4.element.NavigableString):
                        player_name = row.select("a")
                        player_urls.append(player_name[0]['href'])
        else:
            response.raise_for_status()
    return player_urls

def get_player_info(url):
    """Fetch a player's information from bbref and return a dict of dicts containing personal and player information"""
    player_response = requests.get("https://www.basketball-reference.com" + url)
    player_soup = bs4.BeautifulSoup(player_response.text, 'html.parser')
    
    person = {}
    player = {}
    
    image_url = player_soup.find(attrs={"itemscope": "image"})
    if image_url is not None:
        player['image_url'] = image_url['src']
    
    player_info = player_soup.find(attrs={"itemtype": "https://schema.org/Person"})
    name = player_info.find("h1").get_text().split(" ")
    player_info = player_info("p")
    person['preferred_name'] = name[0]
    if len(name) < 2:
        name.append("Hilario")
    last_name = name[1]
    
    raw_info = []
    for info in player_info:
        raw_info.append(info.get_text().replace("\n", " "))
    ignore = ['Pronunciation', 'High School', 'Hall of Fame', 'Draft', 'Experience', 'Relatives', 'Died', 'Recruiting', '(born']

    for info in raw_info:
        if any(string in info for string in ignore):
            continue
        # clean up info
        info = info.replace("\xa0", " ").split(" ")
        info_arr = [x for x in info if x]

        if last_name in info_arr:
            full_name = " ".join(info_arr).split('▪')[0].split(" ")
            last_name_idx = full_name.index(last_name)
            person["last_name"] = " ".join(full_name[last_name_idx:]).strip().strip("I").strip().replace("Jr.", "").strip()
            person["middle_name"] = " ".join(full_name[1:last_name_idx]).strip()
            person["first_name"] = full_name[0]
            
            # players with 3 names (and James Michael McAdoo)
            special_names = ["Carlos Navarro", "John Ramos", "Ray Richardson", "Michael Ray McAdoo", "Vander Velden"]
            if person["last_name"] in special_names or re.search(r"^[vV][ao]n ", person["last_name"]):
                names = person["last_name"].split(" ")
                person["middle_name"] = " ".join(names[0:-1])
                person["preferred_name"] = person["preferred_name"] + " " + names[0]
                person["last_name"] = names[-1]
                
        if 'Position:' in info_arr:
            positions = {
                "Point": "PG", 
                "Shooting": "SG", 
                "Small" : "SF", 
                "Power" : "PF",
                "Center": "C",
                "Guard": "G",
                "Forward": "F"
            }
            player["shooting_hand"] = info_arr[-1]
            block_idx = info_arr.index("▪")
            position_string = " ".join(info_arr[1:block_idx])
            position_list = re.findall(r"[\w']+", " ".join(position_string.split("and")))
            player_positions = set()
            for pos in position_list:
                player_positions.add(positions[pos])
            player["positions"] = list(player_positions)

        if 'kg' in " ".join(info_arr):
            player["weight"] = float(info_arr[-1].split("kg")[0])
            player["height"] = float(info_arr[-2].split("cm")[0][1:])

        if 'Born:' in info_arr:
            birth_date = " ".join(info_arr[1:4])
            person["dob"] = birth_date
            if len(info_arr) > 4:
                in_idx = info_arr.index("in")
                person["birth_place"] = " ".join(info_arr[in_idx+1:-1])

        if 'College:' in info_arr or 'Colleges:' in info_arr:
            person["college"] = " ".join(info_arr[1:])
            
        if 'Debut:' in info_arr:
            debut_info = " ".join(info_arr).split("&blacksquare")
            if len(debut_info) > 1:
                debut_info[1] = debut_info[1].strip().split(" ")
                player["rookie_season"] = int(debut_info[1][-1]) + 1
            else:
                player["rookie_season"] = int(info_arr[-1]) + 1
        
        if 'ABA' in info_arr:
            player['aba'] = True
    
    if 'aba' not in player:
        player['aba'] = False

    player_seasons = player_soup.find_all(attrs={"data-stat": "season", "scope":"row", "class": "left"})
    player_seasons = [season for season in player_seasons if season("a")]
    final_season = player_seasons[-1].get_text()
    final_season = int(final_season[0:2] + final_season[-2:])
    if final_season != 2019:
        player['final_season'] = final_season
    
    return {'player': player, 'person': person }

def get_season_dates(year):
    """Return list of season start and playoff start dates for NBA season ending in year"""
    url = f"https://en.wikipedia.org/wiki/{year-1}-{year % 100}_NBA_season"
    if year % 100 < 10:
        url = f"https://en.wikipedia.org/wiki/{year-1}-0{year % 100}_NBA_season"
    response = requests.get(url)
    if response.status_code == 200:
        season_soup = bs4.BeautifulSoup(response.text, 'html.parser')
        dates = season_soup("table", class_="infobox")[0].select("tbody tr")[3]
        date_string = None
        for i,d in enumerate(dates):
            if i != 0:
                date_string = d.get_text(separator="\n")
        date_list = date_string.split("\n")
        date_list = [date.replace("\xa0", " ").replace(" (Playoffs)", "").strip() for date in date_list]
        season_start = date_list[0].split(" – ")[0].strip()
        if year == 1999:
            season_start += " 1999"
        playoff_start = date_list[1].split("–")[0].strip()
        if playoff_start[-4:] != str(year):
            playoff_start += f" {year}"
        est = pytz.timezone('America/New_York')
        season_start = parse(season_start)
        season_start = est.localize(season_start)
        playoff_start = parse(playoff_start)
        playoff_start = est.localize(playoff_start)
    else:
        response.raise_for_status()
    return [season_start, playoff_start]
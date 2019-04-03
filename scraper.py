import requests, bs4, re, pytz, csv
from util import get_datetime

def get_box_score_urls(season=2019):
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
        info = { 
            'home_stats': {}, 
            'away_stats': {} 
            } 
        
        teams = box_soup.find("h1").get_text().split(' at ')
        teams[1] = teams[1].split(" Box Score, ")[0]
        info['away_team'], info['home_team'] = teams
        
        tables = box_soup("tbody")
        footers = box_soup("tfoot")
        for (i, table) in enumerate(tables):
            team_data = {}
    
            table = [row for row in table.children if isinstance(row, bs4.element.Tag) and len(row.select("a")) > 0]
            for row in table:
                stats = row.select("td")
                if len(stats) > 1:
                    data_row = [str_to_data(stat.text) for stat in stats if stat.text != '']
                name = row.select("a")[0].text
                team_data[name] = data_row
            
            footer = [row for row in footers[i].children if isinstance(row, bs4.element.Tag)]
            for row in footer:
                stats = row(class_="right")
                team_data['Team Totals'] = [str_to_data(stat.text) for stat in stats if stat.text != '']
                team_data['Team Totals'][0] *= 60
            
            if i % 2 == 0:
                box_type = 'basic'
            else:
                box_type = 'advanced'
            if i < 2:
                team_stats = 'away_stats'
            else:
                team_stats = 'home_stats'
            
            info[team_stats][box_type] = team_data
        
        scores = box_soup.find(id="all_line_score")
        score = [s for s in scores if isinstance(s, bs4.element.Comment)][0]
        score_soup = bs4.BeautifulSoup(score, 'html.parser')
        all_quarters = score_soup("td")
        num_periods = int(len(all_quarters)/2 - 2)
        away_quarters = all_quarters[1:num_periods+1]
        away_quarters = [int(q.text) for q in away_quarters]
        home_quarters = all_quarters[num_periods+3:-1]
        home_quarters = [int(q.text) for q in home_quarters]
        info['scoring'] = { 'away': away_quarters, 'home': home_quarters }
        
        scorebox = box_soup.find(class_="scorebox_meta")
        info['tipoff'] = get_datetime(scorebox.div.get_text())
        info['location'] = scorebox.div.next_sibling.get_text().split(",")[0]
        

        misc_info = box_soup.find(text="Inactive:").parent.parent
        misc_info = misc_info.text.replace("\xa0", " ").split("\n")
        misc_info = [el for el in misc_info if el]
        info['attendance'] = int(misc_info[-2].split(": ")[-1].replace(",", ""))
        info['officials'] = misc_info[2][11:].split(", ")

        inactives = misc_info[1].split("   ")
        info['away_stats']['inactive'] = inactives[0][4:].split(", ")
        info['home_stats']['inactive'] = inactives[1][4:].split(", ")
        
        game_length = misc_info[-1].split(": ")[-1]
        game_length = game_length.split(":")
        info['duration'] = 60 * int(game_length[0]) + int(game_length[1])
        

    else:
        response.raise_for_status()
    return info

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
            special_names = ["Jo English", "Rod Hundley", "Carlos Navarro", "John Ramos", "Ray Richardson", "Michael Ray McAdoo", "Vander Velden", "Rod Williams"]
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
                debut_years = [info.split(" ")[-1] for info in debut_info]
                if debut_years[0] < debut_years[1]:
                    debut_idx = 0
                else:
                    debut_idx = 1
                debut_info = debut_info[debut_idx].strip().split(" ")
                debut_date = get_datetime(debut_info[-1].split(":")[-1])
                player['aba'] = True
            else:
                debut_date = get_datetime(debut_info[-1].split(":")[-1])
                player['aba'] = False
            rookie_year = debut_date.year + 1
            if debut_date.month < 7:
                rookie_year -= 1
            player["rookie_season"] = rookie_year


    player_seasons = player_soup.find_all(attrs={"data-stat": "season", "scope":"row", "class": "left"})
    player_seasons = [season for season in player_seasons if season("a")]
    final_season = player_seasons[-1].get_text()
    final_season = int(final_season[0:2] + final_season[-2:])
    if final_season == 1900:
        final_season = 2000
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
        season_start = get_datetime(season_start)
        playoff_start = get_datetime(playoff_start)
    else:
        response.raise_for_status()
    return [season_start, playoff_start]

def save_season_info():
    with open('data/season_info.csv', mode='w') as file:
        writer = csv.writer(file, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for year in range(1947, 2020):
            i = year - 1946
            season_start, playoff_start = get_season_dates(year)
            season_info = [i, 1, year, season_start, playoff_start]
            writer.writerow(season_info)
        start_dates = ["October 13, 1967", "October 18, 1968", "October 17, 1969", "October 14, 1970", "October 13, 1971", "October 12, 1972", "October 10, 1973", "October 18, 1974", "October 24, 1975"]
        playoff_dates = ["March 23, 1968", "April 5, 1969", "April 17, 1970", "April 1, 1971", "March 31, 1972", "March 30, 1973", "March 29, 1974", "April 4, 1975", "April 8, 1976"]
        i += 1
        for year in range(1968, 1977):
            j = year - 1968
            season_info = [i, 2, year, get_datetime(start_dates[j]), get_datetime(playoff_dates[j])]
            writer.writerow(season_info)
            i += 1

def str_to_data(el):
    if '.' in el:
        return float(el)
    elif ':' in el:
        stat = el.split(":")
        return 60 * int(stat[0]) + int(stat[1])
    else:
        return int(el)
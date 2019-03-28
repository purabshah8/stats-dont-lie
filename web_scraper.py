import requests
import bs4
import re
from seed import insert

def get_box_score_urls(season="2019"):
    months = ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may', 'june']
    # months = ['october', 'november', 'december', 'january', 'february', 'march']
    urls = []
    for month in months:
        response = requests.get("https://www.basketball-reference.com/leagues/NBA_{0}_games-{1}.html".format(season,month))
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
        response = requests.get("https://www.basketball-reference.com/players/{0}/".format(letter))
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
    player_response = requests.get("https://www.basketball-reference.com" + url)
    player_soup = bs4.BeautifulSoup(player_response.text, 'html.parser')
    player_info = player_soup.find(attrs={"itemtype": "https://schema.org/Person"})
    
    name = player_info.find("h1")
    name = name.get_text().split(" ")
    player_info = player_info("p")
    player = {"preferred_name": name[0]}
    last_name = name[1]
    
    raw_info = []
    for info in player_info:
        raw_info.append(info.get_text().replace("\n", " "))
    info_topics = ['Pronunciation', 'High School', 'Hall of Fame', 'Draft', 'Experience', 'Relatives', 'Died', 'Recruiting', '(born']

    for info in raw_info:
        if any(string in info for string in info_topics):
            continue
        info = info.replace("\xa0", " ").split(" ")
        info_arr = [x for x in info if x]

        if last_name in info_arr:
            full_name = " ".join(info_arr).split('▪')[0].split(" ")
            last_name_idx = full_name.index(last_name)
            print(full_name)
            player["last_name"] = " ".join(full_name[last_name_idx:]).strip().strip("I").strip().replace("Jr.", "").strip()
            player["middle_name"] = " ".join(full_name[1:last_name_idx]).strip()
            player["first_name"] = full_name[0]
            print(player["last_name"])
            # special cases 
            special_names = ["Carlos Navarro", "John Ramos", "Ray Richardson", "Michael Ray McAdoo", "Vander Velden"]
            
            if player["last_name"] in special_names or re.search(r"^[vV][ao]n ", player["last_name"]):
                names = player["last_name"].split(" ")
                player["middle_name"] = " ".join(names[0:-1])
                player["preferred_name"] = player["preferred_name"] + " " + names[0]
                player["last_name"] = names[-1]
                
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
            shooting_hand = info_arr[-1]
            player["shooting_hand"] = shooting_hand
            block_idx = info_arr.index("▪")
            position_string = " ".join(info_arr[1:block_idx])
            position_list = re.findall(r"[\w']+", " ".join(position_string.split("and")))
            player_positions = set()
            for pos in position_list:
                player_positions.add(positions[pos])
            player["positions"] = list(player_positions)

        if 'kg' in " ".join(info_arr):
            weight = float(info_arr[-1].split("kg")[0])
            player["weight"] = weight
            height = float(info_arr[-2].split("cm")[0][1:])
            player["height"] = height

        if 'Born:' in info_arr:
            birth_date = " ".join(info_arr[1:4])
            player["birth_date"] = birth_date
            if len(info_arr) > 4:
                in_idx = info_arr.index("in")
                birth_place = " ".join(info_arr[in_idx+1:-1])
                player["birth_place"] = birth_place

        if 'College:' in info_arr or 'Colleges:' in info_arr:
            college = " ".join(info_arr[1:])
            player["college"] = college
            
        if 'Debut:' in info_arr:
            debut_info = " ".join(info_arr).split("&blacksquare")
            if len(debut_info) > 1:
                debut_info[0] = debut_info[0].strip().split(" ")
                debut_info[1] = debut_info[1].strip().split(" ")
                player["nba_debut"] = int(debut_info[0][-1]) + 1
                player["aba_debut"] = int(debut_info[1][-1]) + 1
            else:
                player["nba_debut"] = int(info_arr[-1]) + 1
                
    return player

if __name__ == "__main__":

    player_urls = get_player_urls()
    for url in player_urls:
        player_info = get_player_info(url)
        insert('player', player_info)

    box_score_urls = get_box_score_urls(2019)
    for url in box_score_urls:
        basic, advanced = get_box_score_info(url)
        insert('basic_box', basic)
        insert('advanced_box', advanced)

import os, sys, django, psycopg2, pytz, csv, datetime
from dateutil.parser import parse
from util import get_datetime, ABA_TEAMS
from scraper import get_season_dates

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statsdontlie.settings")
django.setup()

connection_url = os.environ["DATABASE_URL"]
if os.environ.get('DJANGO_DEVELOPMENT') is not None:
    connection_url = "dbname=nba user=purab password=godricshallows"



leagues = [
    (1, "nba", 1946),
    (2, "aba", 1967)
    ]

conferences = [
    (1, "Eastern Conference", "East", 1),
    (2, "Western Conference", "West", 1),
]

divisions = [
    (1, "Atlantic Division", "ATL", 1),
    (2, "Central Division", "CEN", 1),
    (3, "Southeast Division", "SE", 1),
    (4, "Southwest Division", "SW", 1),
    (5, "Nortwest Division", "NW", 1),
    (6, "Pacific Division", "PAC", 1),
]

locations = [
    (1, "address", "601 Biscayne Boulevard", "Miami", "FL", "USA", 33132),
    (2, "address", "2500 Victory Avenue", "Dallas", "TX", "USA", 75219),
    (3, "address", "400 W Church Street", "Orlando", "FL", "USA", 32801),
    (4, "address", "1 AT&T Center Parkway", "San Antonio", "TX", "USA", 78219),
    (5, "address", "125 South Pennsylvania Street", "Indianapolis", "IN", "USA", 46204),
    (6, "address", "620 Atlantic Avenue", "Brooklyn", "NY", "USA", 11217),
    (7, "address", "601 F Street NW", "Washington", "DC", "USA", 20004),
    (8, "address", "100 W Reno Avenue", "Oklahoma City", "OK", "USA", 73102),
    (9, "address", "191 Beale Street", "Memphis", "TN", "USA", 38103),
    (10, "address", "1111 Vel R. Phillips Avenue", "Milwaukee", "WI", "USA", 53203),
    (11, "address", "500 David J. Stern Walk", "Sacramento", "CA", "USA", 95814),
    (12, "address", "2645 Woodward Ave", "Detroit", "MI", "USA", 48201),
    (13, "address", "4 Pennsylvania Plaza", "New York", "NY", "USA", 10001),
    (14, "address", "1 Center Court", "Portland", "OR", "USA", 97227),
    (15, "address", "7000 Coliseum Way", "Oakland", "CA", "USA", 94621),
    (16, "address", "1000 Chopper Circle", "Denver", "CO", "USA", 80204),
    (17, "address", "1 Center Ct", "Cleveland", "OH", "USA", 44115),
    (18, "address", "40 Bay Street", "Toronto", "ON", "Canada", None),
    (19, "address", "1501 Girod Street", "New Orleans", "LA", "USA", 70113),
    (20, "address", "333 East Trade Street", "Charlotte", "NC", "USA", 28202),
    (21, "address", "1111 S. Figueroa Street", "Los Angeles", "CA", "USA", 90015),
    (22, "address", "1 State Farm Drive", "Atlanta", "GA", "USA", 30303),
    (23, "address", "201 East Jefferson Street", "Phoenix", "AZ", "USA", 85004),
    (24, "address", "600 First Avenue North", "Minneapolis", "MN", "USA", 55403),
    (25, "address", "100 Legends Way", "Boston", "MA", "USA", 2114),
    (26, "address", "1510 Polk Street", "Houston", "TX", "USA", 77002),
    (27, "address", "1901 West Madison Street", "Chicago", "IL", "USA", 60612),
    (28, "address", "301 South Temple", "Salt Lake City", "UT", "USA", 84101),
    (29, "address", "3601 South Broad Street", "Philadelphia", "PA", "USA", 19148),
    (30, "address", "305 Harrison Street", "Seattle", "WA", "USA", 98109)
]

arenas = [
    (1, "American Airlines Arena", 1, 19600, 2000),
    (2, "American Airlines Center", 2, 21146, 2002),
    (3, "Amway Center", 3, 18846, 2011),
    (4, "AT&T Center", 4, 18418, 2003),
    (5, "Bankers Life Fieldhouse", 5, 17923, 2000),
    (6, "Barclays Center", 6, 17732, 2013),
    (7, "Capital One Arena", 7, 20356, 1998),
    (8, "Chesapeake Energy Arena", 8, 18203, 2003),
    (9, "FedEx Forum", 9, 17794, 2005),
    (10, "Fiserv Forum", 10, 17500, 2019),
    (11, "Golden 1 Center", 11, 17583, 2017),
    (12, "Little Caesars Arena", 12, 20491, 2018),
    (13, "Madison Square Garden", 13, 19812, 1968),
    (14, "Moda Center", 14, 19441, 1996),
    (15, "Oracle Arena", 15, 19596, 1972),
    (16, "Pepsi Center", 16, 19520, 2000),
    (17, "Quicken Loans Arena", 17, 20562, 1995),
    (18, "Scotiabank Arena", 18, 19800, 2000),
    (19, "Smoothie King Center", 19, 16867, 2000),
    (20, "Spectrum Center", 20, 19077, 2006),
    (21, "Staples Center", 21, 19068, 2000),
    (22, "State Farm Arena", 22, 18118, 2000),
    (23, "Talking Stick Resort Arena", 23, 18055, 1993),
    (24, "Target Center", 24, 18978, 1991),
    (25, "TD Garden", 25, 18624, 1996),
    (26, "Toyota Center", 26, 18055, 2004),
    (27, "United Center", 27, 20917, 1995),
    (28, "Vivint Smart Home Arena", 28, 18306, 1992),
    (29, "Wells Fargo Center", 29, 20478, 1997),
    (30, "Key Arena", 30, 17459, 1962)
]

teams = [
    (1, 1, "Celtics", "Boston", 25, 1947, None, "BOS"),
    (2, 1, "Nets", "Brooklyn", 6, 1968, None, "BKN"),
    (3, 1, "76ers", "Philadelphia", 29, 1947, None, "PHI"),
    (4, 1, "Knicks", "New York", 13, 1947, None, "NYK"),
    (5, 1, "Raptors", "Toronto", 18, 1996, None, "TOR"),
    (6, 2, "Bulls", "Chicago", 27, 1967, None, "CHI"),
    (7, 2, "Cavaliers", "Cleveland", 17, 1971, None, "CLE"),
    (8, 2, "Pistons", "Detroit", 12, 1942, None, "DET"),
    (9, 2, "Pacers", "Indiana", 5, 1968, None, "IND"),
    (10, 2, "Bucks", "Milwaukee", 10, 1969, None, "MIL"),
    (11, 3, "Hawks", "Atlanta", 22, 1947, None, "ATL"),
    (12, 3, "Hornets", "Charlotte", 20, 1989, None, "CHA"),
    (13, 3, "Heat", "Miami", 1, 1989, None, "MIA"),
    (14, 3, "Magic", "Orlando", 3, 1990, None, "ORL"),
    (15, 3, "Wizards", "Washington", 7, 1962, None, "WAS"),
    (16, 4, "Mavericks", "Dallas", 2, 1981, None, "DAL"),
    (17, 4, "Rockets", "Houston", 26, 1968, None, "HOU"),
    (18, 4, "Grizzlies", "Memphis", 9, 1996, None, "MEM"),
    (19, 4, "Pelicans", "New Orleans", 19, 2003, None, "NOP"),
    (20, 4, "Spurs", "San Antonio", 4, 1968, None, "SAS"),
    (21, 5, "Nuggets", "Denver", 16, 1968, None, "DEN"),
    (22, 5, "Timberwolves", "Minnesota", 24, 1990, None, "MIN"),
    (23, 5, "Thunder", "Oklahoma City", 8, 2009, None, "OKC"),
    (24, 5, "Trail Blazers", "Portland", 14, 1971, None, "POR"),
    (25, 5, "Jazz", "Utah", 28, 1975, None, "UTA"),
    (26, 6, "Warriors", "Golden State", 15, 1947, None, "GSW"),
    (27, 6, "Clippers", "Los Angeles", 21, 1971, None, "LAC"),
    (28, 6, "Lakers", "Los Angeles", 21, 1948, None, "LAL"),
    (29, 6, "Suns", "Phoenix", 23, 1969, None, "PHX"),
    (30, 6, "Kings", "Sacramento", 11, 1924, None, "SAC"),
    (31, 6, "Supersonics", "Seattle", 30, 1967, 2008,"SEA")
]

seasons = []
with open("data/season_info.csv") as f:
    csv_reader = csv.reader(f, delimiter="|")
    for row in csv_reader:
        season_start = parse(row[-1])
        playoff_start = parse(row[-2])
        row = [int(col) for col in row[0:3]]
        row.append(season_start)
        row.append(playoff_start)
        seasons.append(tuple(row))

positions = [
    (1, "Point Guard", "PG"),
    (2, "Shooting Guard", "SG"),
    (3, "Small Forward", "SF"),
    (4, "Power Forward", "PF"),
    (5, "Center", "C"),
    (6, "Guard", "G"),
    (7, "Forward", "F"),
]

team_seasons = []
i = 1
for season in seasons:
    year = season[2]
    league_id = season[1]
    if league_id == 1 and year < 1977:
        active_teams = [team for team in teams if team[5] <= year and team[2] not in ABA_TEAMS]
    elif league_id == 2 and year < 1977:
        active_teams = [team for team in teams if team[2] in ABA_TEAMS]
    else:
        active_teams = [team for team in teams if team[5] <= year]
    
    for team in active_teams:
        team_season = (i, team[0], season[0])
        team_seasons.append(team_season)
        i += 1


def insert(table, values):
    connection = None

    try:
        connection = psycopg2.connect("dbname=nba user=purab password=godricshallows", sslmode='require')
        cursor = connection.cursor()
        num_args_str = "(" + "%s," * (len(values[0])-1) + "%s)"
        args = [str(cursor.mogrify(num_args_str, x), "utf-8") for x in values]
        args_str = ",".join(args)
        cursor.execute("INSERT INTO " + table + " VALUES " + args_str)
        connection.commit()
        print("Populated", table, "table")
    except psycopg2.DatabaseError as e:
        if connection:
            connection.rollback()
            print("rolling back...")
        print("Error %s" % e)
        sys.exit(1)
    finally:
        if connection:
            connection.close()

tables = ["league", "conference", "division", "location", "arena", "team", "season", "position", "team_season"]
seed_data = [leagues, conferences, divisions, locations, arenas, teams, seasons, positions, team_seasons]

# if __name__ == "__main__":
#     for i in range(len(seed_data)):
#         insert(tables[i], seed_data[i])
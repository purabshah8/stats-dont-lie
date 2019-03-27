import psycopg2
import sys

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
    (1, "601 Biscayne Boulevard", "Miami", "FL", "USA", 33132),
    (2, "2500 Victory Avenue", "Dallas", "TX", "USA", 75219),
    (3, "400 W Church Street", "Orlando", "FL", "USA", 32801),
    (4, "1 AT&T Center Parkway", "San Antonio", "TX", "USA", 78219),
    (5, "125 South Pennsylvania Street", "Indianapolis", "IN", "USA", 46204),
    (6, "620 Atlantic Avenue", "Brooklyn", "NY", "USA", 11217),
    (7, "601 F Street NW", "Washington", "DC", "USA", 20004),
    (8, "100 W Reno Avenue", "Oklahoma City", "OK", "USA", 73102),
    (9, "191 Beale Street", "Memphis", "TN", "USA", 38103),
    (10, "1111 Vel R. Phillips Avenue", "Milwaukee", "WI", "USA", 53203),
    (11, "500 David J. Stern Walk", "Sacramento", "CA", "USA", 95814),
    (12, "2645 Woodward Ave", "Detroit", "MI", "USA", 48201),
    (13, "4 Pennsylvania Plaza", "New York", "NY", "USA", 10001),
    (14, "1 Center Court", "Portland", "OR", "USA", 97227),
    (15, "7000 Coliseum Way", "Oakland", "CA", "USA", 94621),
    (16, "1000 Chopper Circle", "Denver", "CO", "USA", 80204),
    (17, "1 Center Ct", "Cleveland", "OH", "USA", 44115),
    (18, "40 Bay Street", "Toronto", "ON", "Canada", None),
    (19, "1501 Girod Street", "New Orleans", "LA", "USA", 70113),
    (20, "333 East Trade Street", "Charlotte", "NC", "USA", 28202),
    (21, "1111 S. Figueroa Street", "Los Angeles", "CA", "USA", 90015),
    (22, "1 State Farm Drive", "Atlanta", "GA", "USA", 30303),
    (23, "201 East Jefferson Street", "Phoenix", "AZ", "USA", 85004),
    (24, "600 First Avenue North", "Minneapolis", "MN", "USA", 55403),
    (25, "100 Legends Way", "Boston", "MA", "USA", 2114),
    (26, "1510 Polk Street", "Houston", "TX", "USA", 77002),
    (27, "1901 West Madison Street", "Chicago", "IL", "USA", 60612),
    (28, "301 South Temple", "Salt Lake City", "UT", "USA", 84101),
    (29, "3601 South Broad Street", "Philadelphia", "PA", "USA", 19148),
]

arenas = [
    (1, "American Airlines Arena", 1, 19600, 2000), # 54 => 1
    (2, "American Airlines Center", 2, 21146, 2002),
    (3, "Amway Center", 3, 18846, 2011),
    (4, "AT&T Center", 4, 18418, 2003),
    (5, "Bankers Life Fieldhouse", 5, 17923, 2000), # 58 => 5
    (6, "Barclays Center", 6, 17732, 2013),
    (7, "Capital One Arena", 7, 20356, 1998),
    (8, "Chesapeake Energy Arena", 8, 18203, 2003),
    (9, "FedEx Forum", 9, 17794, 2005),
    (10, "Fiserv Forum", 10, 17500, 2019), # 63 => 10
    (11, "Golden 1 Center", 11, 17583, 2017),
    (12, "Little Caesars Arena", 12, 20491, 2018),
    (13, "Madison Square Garden", 13, 19812, 1968),
    (14, "Moda Center", 14, 19441, 1996),
    (15, "Oracle Arena", 15, 19596, 1972), # 68 => 15
    (16, "Pepsi Center", 16, 19520, 2000),
    (17, "Quicken Loans Arena", 17, 20562, 1995),
    (18, "Scotiabank Arena", 18, 19800, 2000),
    (19, "Smoothie King Center", 19, 16867, 2000),
    (20, "Spectrum Center", 20, 19077, 2006), # 73 => 20
    (21, "Staples Center", 21, 19068, 2000),
    (22, "State Farm Arena", 22, 18118, 2000),
    (23, "Talking Stick Resort Arena", 23, 18055, 1993),
    (24, "Target Center", 24, 18978, 1991),
    (25, "TD Garden", 25, 18624, 1996), # 78 => 25
    (26, "Toyota Center", 26, 18055, 2004),
    (27, "United Center", 27, 20917, 1995),
    (28, "Vivint Smart Home Arena", 28, 18306, 1992),
    (29, "Wells Fargo Center", 29, 20478, 1997), # 82 => 29
]

teams = [
    (1, 1, "Celtics", "Boston", 25, 1947, "BOS"),
    (2, 1, "Nets", "Brooklyn", 6, 1968, "BKN"),
    (3, 1, "76ers", "Philadelphia", 29, 1947, "PHI"),
    (4, 1, "Knicks", "New York", 13, 1947, "NYK"),
    (5, 1, "Raptors", "Toronto", 18, 1996, "TOR"),
    (6, 2, "Bulls", "Chicago", 27, 1967, "CHI"),
    (7, 2, "Cavaliers", "Cleveland", 17, 1971, "CLE"),
    (8, 2, "Pistons", "Detroit", 12, 1942, "DET"),
    (9, 2, "Pacers", "Indiana", 5, 1968, "IND"),
    (10, 2, "Bucks", "Milwaukee", 10, 1969, "MIL"),
    (11, 3, "Hawks", "Atlanta", 22, 1947, "ATL"),
    (12, 3, "Hornets", "Charlotte", 20, 1989, "CHA"),
    (13, 3, "Heat", "Miami", 1, 1989, "MIA"),
    (14, 3, "Magic", "Orlando", 3, 1990, "ORL"),
    (15, 3, "Wizards", "Washington", 7, 1962, "WAS"),
    (16, 4, "Mavericks", "Dallas", 2, 1981, "DAL"),
    (17, 4, "Rockets", "Houston", 26, 1968, "HOU"),
    (18, 4, "Grizzlies", "Memphis", 9, 1996, "MEM"),
    (19, 4, "Pelicans", "New Orleans", 19, 2003, "NOP"),
    (20, 4, "Spurs", "San Antonio", 4, 1968, "SAS"),
    (21, 5, "Nuggets", "Denver", 16, 1968, "DEN"),
    (22, 5, "Timberwolves", "Minnesota", 24, 1990, "MIN"),
    (23, 5, "Thunder", "Oklahoma City", 8, 2009, "OKC"),
    (24, 5, "Trail Blazers", "Portland", 14, 1971, "POR"),
    (25, 5, "Jazz", "Utah", 28, 1975, "UTA"),
    (26, 6, "Warriors", "Golden State", 15, 1947, "GSW"),
    (27, 6, "Clippers", "Los Angeles", 21, 1971, "LAC"),
    (28, 6, "Lakers", "Los Angeles", 21, 1948, "LAL"),
    (29, 6, "Suns", "Phoenix", 23, 1969, "PHX"),
    (30, 6, "Kings", "Sacramento", 11, 1924, "SAC"),
]

def insert(table, values):
    connection = None

    try:
        connection = psycopg2.connect("dbname=nba user=purab password=godricshallows")
        cursor = connection.cursor()
        num_args_str = "(" + "%s," * (len(values[0])-1) + "%s)"
        args = [str(cursor.mogrify(num_args_str, x), 'utf-8') for x in values]
        args_str = ','.join(args)
        cursor.execute("INSERT INTO " + table + " VALUES " + args_str)
        connection.commit()
        print("Populated", table, "table")
    except psycopg2.DatabaseError as e:
        if connection:
            connection.rollback()
            print("rolling back...")
        print('Error %s' % e)
        sys.exit(1)
    finally:
        if connection:
            connection.close()

tables = ["league", "conference", "division", "location", "arena", "team", "season", "person", "team_employee", "referee", "player", "position", "player_position"]

seed_data = [leagues, conferences, divisions, locations, arenas, teams]
for i in range(len(seed_data)):
    insert(tables[i], seed_data[i])
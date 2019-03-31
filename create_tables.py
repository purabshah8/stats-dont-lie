import psycopg2
import sys


def create_tables():
    commands = [
        """
            DROP TABLE IF EXISTS 
                league, conference, division, 
                location, arena, team, season, 
                person, team_employee, referee,
                player, position, player_position;
        """,
        """ 
            CREATE TABLE league(
                id SERIAL PRIMARY KEY,
                name VARCHAR(8) NOT NULL,
                year_founded INTEGER NOT NULL
            );
        """,
        """ 
            CREATE TABLE conference(
                id SERIAL PRIMARY KEY,
                name VARCHAR(32) NOT NULL,
                abbreviation VARCHAR(8) NOT NULL,
                league_id INTEGER NOT NULL
                    REFERENCES league(id)
                    ON DELETE CASCADE ON UPDATE CASCADE
            );
        """,
        """ 
            CREATE TABLE division(
                id SERIAL PRIMARY KEY,
                name VARCHAR(32) NOT NULL,
                abbreviation VARCHAR(8) NOT NULL,
                conference_id INTEGER NOT NULL
                    REFERENCES conference(id)
                    ON DELETE CASCADE ON UPDATE CASCADE
            );
        """,
        """ 
            CREATE TABLE location(
                id SERIAL PRIMARY KEY,
                precision VARCHAR(32) NOT NULL,
                address TEXT,
                city VARCHAR(64),
                state VARCHAR(64),
                country VARCHAR(64) NOT NULL,
                postal_code INTEGER
            );
        """,
        """ 
            CREATE TABLE arena(
                id SERIAL PRIMARY KEY,
                name VARCHAR(64),
                location_id INTEGER NOT NULL
                    REFERENCES location(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                capacity INTEGER NOT NULL,
                year_opened INTEGER NOT NULL,
                year_closed INTEGER
            );
        """,
        """ 
            CREATE TABLE team(
                id SERIAL PRIMARY KEY,
                division_id INTEGER NOT NULL
                    REFERENCES division(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                name VARCHAR(16) NOT NULL,
                city VARCHAR(16) NOT NULL,
                arena_id INTEGER NOT NULL
                    REFERENCES arena(id) 
                    ON DELETE CASCADE ON UPDATE CASCADE,
                year_founded INTEGER NOT NULL,
                abbreviation VARCHAR(8) NOT NULL
            );
        """,
        """
            CREATE TABLE season(
                id SERIAL PRIMARY KEY,
                league_id INTEGER NOT NULL
                    REFERENCES league(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                year INTEGER NOT NULL,
                season_start DATE,
                playoff_start DATE
            );
        """,
        """ 
            CREATE TABLE person(
                id SERIAL PRIMARY KEY,
                last_name VARCHAR(32) NOT NULL,
                first_name VARCHAR(32) NOT NULL,
                middle_name VARCHAR(32),
                preferred_name VARCHAR(32),
                dob DATE NOT NULL,
                college VARCHAR(64),
                birthplace_id INTEGER NOT NULL
                    REFERENCES location(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE
            );
        """,
        """
            CREATE TABLE team_employee(
                id INTEGER NOT NULL PRIMARY KEY
                    REFERENCES person(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                team_id INTEGER NOT NULL
                    REFERENCES team(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                role VARCHAR(16) NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE
            );
        """,
        """ 
            CREATE TABLE referee(
                id INTEGER NOT NULL PRIMARY KEY
                    REFERENCES person(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                jersey_number INTEGER NOT NULL,
                rookie_season_id INTEGER NOT NULL
                    REFERENCES season(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE
            );
        """,
        """ 
            CREATE TABLE player(
                id INTEGER NOT NULL PRIMARY KEY
                    REFERENCES person(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                height INTEGER NOT NULL,
                weight INTEGER NOT NULL,
                shooting_hand VARCHAR(5) NOT NULL,
                rookie_season_id INTEGER NOT NULL
                    REFERENCES season(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                final_season_id INTEGER NOT NULL
                    REFERENCES season(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                image_url VARCHAR(128) NOT NULL
            );
        """,
        """
            CREATE TABLE position(
                id INTEGER NOT NULL PRIMARY KEY,
                name VARCHAR(16) NOT NULL,
                abbreviation VARCHAR(2) NOT NULL
            );
        """,
        """ 
            CREATE TABLE player_position(
                id SERIAL PRIMARY KEY,
                player_id INTEGER NOT NULL
                    REFERENCES player(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                position_id INTEGER NOT NULL
                    REFERENCES position(id)
                    ON DELETE CASCADE ON UPDATE CASCADE
            );
        """
    ]

    connection = None
    try:
        connection = psycopg2.connect("dbname=nba user=purab password=godricshallows")
        cursor = connection.cursor()
        tables = ["league", "conference", "division", "location", "arena", "team", "season", "person", "team_employee", "referee", "player", "position", "player_position"]
        for i, command in enumerate(commands):
            cursor.execute(command)
            if i == 0:
                print("Dropping existing tables...")
            else:
                print("Created table", tables[i-1])
        
        cursor.close()
        connection.commit()
    except psycopg2.DatabaseError as e:
        if connection:
            connection.rollback()
            print("rolling back...")
        print('Error %s' % e)
        sys.exit(1)
    finally:
        if connection:
            connection.close()



if __name__ == '__main__':
    create_tables()

# commands = [
#     """ 
#         CREATE TABLE table_name(
#             id SERIAL PRIMARY KEY,

#         );
#     """,
#     """
#         CREATE TABLE logo(
#             id SERIAL PRIMARY KEY,
#             url TEXT NOT NULL,
#             team_id INTEGER NOT NULL
#                 REFERENCES team(id)
#                 ON DELETE CASCADE ON UPDATE CASCADE,
#             type VARCHAR(32) NOT NULL,
#             debut_year INTEGER,
#             final_year INTEGER
#         );
#     """,
# ]
import psycopg2
import sys
import os

connection_url = os.environ.get("DATABASE_URL")
if os.environ.get('DJANGO_DEVELOPMENT') is not None:
    connection_url = "dbname=nba user=purab password=godricshallows"

def create_tables():
    commands = [
        """
            DROP TABLE IF EXISTS 
                league, conference, division, location, arena, 
                team, season, person, team_employee, referee, 
                player, position, player_position, team_season, 
                player_team_season, game, game_period, 
                statline, player_statline CASCADE;
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
                year_defunct INTEGER,
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
                start_date TIMESTAMP,
                playoffs_start_date TIMESTAMP
            );
        """,
        """ 
            CREATE TABLE person(
                id SERIAL PRIMARY KEY,
                last_name VARCHAR(32) NOT NULL,
                first_name VARCHAR(32) NOT NULL,
                middle_name VARCHAR(32),
                preferred_name VARCHAR(32),
                dob DATE,
                college TEXT,
                birthplace_id INTEGER
                    REFERENCES location(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE
            );
        """,
        """
            CREATE TABLE team_employee(
                person_id INTEGER NOT NULL PRIMARY KEY
                    REFERENCES person(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
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
                person_id INTEGER NOT NULL PRIMARY KEY
                    REFERENCES person(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                jersey_number INTEGER,
                rookie_season_id INTEGER NOT NULL
                    REFERENCES season(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                final_season_id INTEGER
                    REFERENCES season(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE
            );
        """,
        """ 
            CREATE TABLE player(
                person_id INTEGER NOT NULL PRIMARY KEY
                    REFERENCES person(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                height INTEGER NOT NULL,
                weight INTEGER NOT NULL,
                shooting_hand VARCHAR(5) NOT NULL,
                rookie_season_id INTEGER NOT NULL
                    REFERENCES season(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                final_season_id INTEGER
                    REFERENCES season(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                image_url VARCHAR(128)
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
                    REFERENCES person(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                position_id INTEGER NOT NULL
                    REFERENCES position(id)
                    ON DELETE CASCADE ON UPDATE CASCADE
            );
        """,
        """ 
            CREATE TABLE team_season(
                id SERIAL PRIMARY KEY,
                team_id INTEGER NOT NULL
                    REFERENCES team(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                season_id INTEGER NOT NULL
                    REFERENCES season(id)
                    ON DELETE CASCADE ON UPDATE CASCADE
            );
        """,
        """ 
            CREATE TABLE player_team_season(
                id SERIAL PRIMARY KEY,
                player_id INTEGER NOT NULL
                    REFERENCES person(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                team_season_id INTEGER NOT NULL
                    REFERENCES team_season(id)
                    ON DELETE CASCADE ON UPDATE CASCADE
            );
        """,
        """ 
            CREATE TABLE game(
                id VARCHAR(16) PRIMARY KEY,
                home_id INTEGER NOT NULL
                    REFERENCES team(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                away_id INTEGER NOT NULL
                    REFERENCES team(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                home_score INTEGER NOT NULL,
                away_score INTEGER NOT NULL,
                winner_id INTEGER NOT NULL
                    REFERENCES team(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                ref_one_id INTEGER
                    REFERENCES person(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                ref_two_id INTEGER
                    REFERENCES person(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                ref_three_id INTEGER
                    REFERENCES person(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE,
                tipoff TIMESTAMP,
                attendance INTEGER,
                duration INTEGER
            );
        """,
        """ 
            CREATE TABLE game_period(
                game_id VARCHAR(16) NOT NULL
                    REFERENCES game(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                number INTEGER NOT NULL,
                home_score INTEGER NOT NULL,
                away_score INTEGER NOT NULL,
                PRIMARY KEY(game_id, number)
            );
        """,
        """ 
            CREATE TABLE statline(
                id SERIAL PRIMARY KEY,
                game_id VARCHAR(16) NOT NULL
                    REFERENCES game(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                team_id INTEGER NOT NULL
                    REFERENCES team(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                mp INTEGER,
                fg INTEGER,
                fga INTEGER,
                fg_pct FLOAT,
                tp INTEGER,
                tpa INTEGER,
                tp_pct FLOAT,
                ft INTEGER,
                fta INTEGER,
                ft_pct FLOAT,
                orb INTEGER,
                drb INTEGER,
                trb INTEGER,
                ast INTEGER,
                stl INTEGER,
                blk INTEGER,
                tov INTEGER,
                pf INTEGER,
                pts INTEGER,
                poss FLOAT,
                ts FLOAT,
                efg FLOAT,
                tpar FLOAT,
                ftr FLOAT,
                orb_pct FLOAT,
                drb_pct FLOAT,
                trb_pct FLOAT,
                ast_pct FLOAT,
                stl_pct FLOAT,
                blk_pct FLOAT,
                tov_pct FLOAT,
                usg_rate FLOAT,
                ortg FLOAT,
                drtg FLOAT
            );
        """,
        """ 
            CREATE TABLE player_statline(
                statline_id INTEGER NOT NULL PRIMARY KEY
                    REFERENCES statline(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                player_id INTEGER NOT NULL
                    REFERENCES person(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                started BOOL NOT NULL,
                plus_minus integer NOT NULL
            );
        """,
    ]

    connection = None
    try:
        if os.environ.get('DJANGO_DEVELOPMENT') is not None:
            connection = psycopg2.connect(connection_url)
        else:
            connection = psycopg2.connect(connection_url, sslmode='require')
        cursor = connection.cursor()
        tables = ["league", "conference", "division", "location", "arena", "team", "season", "person", "team_employee", "referee", "player",
                  "position", "player_position", "team_season", "player_team_season", "game", "game_period", "statline", "player_statline"]
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


def execute_command(command):
    connection = None
    try:
        if os.environ.get('DJANGO_DEVELOPMENT') is not None:
            connection = psycopg2.connect(connection_url)
        else:
            connection = psycopg2.connect(connection_url, sslmode='require')
        cursor = connection.cursor()
        cursor.execute(command)
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
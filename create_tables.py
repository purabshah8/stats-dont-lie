import psycopg2
import sys


def create_tables():
    commands = [
        """
            DROP TABLE IF EXISTS league, conference, division, location, arena, team, logo;
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
            CREATE TABLE logo(
                id SERIAL PRIMARY KEY,
                url TEXT NOT NULL,
                team_id INTEGER NOT NULL
                    REFERENCES team(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                type VARCHAR(32) NOT NULL,
                debut_year INTEGER,
                final_year INTEGER
            );
        """,
    ]

    connection = None
    try:
        connection = psycopg2.connect("dbname=nba user=purab password=godricshallows")
        cursor = connection.cursor()
        tables = ["league", "conference", "division", "location", "arena", "team", "logo"]
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
# """ 
#             CREATE TABLE table_name(
#                 id SERIAL PRIMARY KEY,
                
#             );
#         """,
#         """ 
#             CREATE TABLE table_name(
#                 id SERIAL PRIMARY KEY,
                
#             );
#         """,
#         """ 
#             CREATE TABLE table_name(
#                 id SERIAL PRIMARY KEY,

#             );
#         """,
#         """ 
#             CREATE TABLE table_name(
#                 id SERIAL PRIMARY KEY,
                
#             );
#         """,
#         """ 
#             CREATE TABLE table_name(
#                 id SERIAL PRIMARY KEY,

#             );
#         """,
#         """ 
#             CREATE TABLE table_name(
#                 id SERIAL PRIMARY KEY,
                
#             );
#         """,
# ]
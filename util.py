import os
import sys
import django
import psycopg2
import pytz
from dateutil.parser import parse
from django.utils.six import StringIO

connection_url = os.environ.get("DATABASE_URL")
if os.environ.get("DJANGO_DEVELOPMENT") is not None:
    connection_url = "dbname=nba user=purab password=godricshallows"

ABA_TEAMS = ["Nets", "Spurs", "Pacers", "Nuggets"]

NBA_MONTHS = ["october", "november", "december", "january", "february", "march", "april", "may", "june"]

STATES = ["Alabama", "Alaska", "American Samoa", "Arizona", "Arkansas",
          "California", "Colorado", "Connecticut", "Delaware",
          "District of Columbia", "Federated States of Micronesia", "Florida",
          "Georgia", "Guam", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
          "Kansas", "Kentucky", "Louisiana", "Maine", "Marshall Islands",
          "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
          "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
          "New Jersey", "New Mexico", "New York", "North Carolina",
          "North Dakota", "Northern Mariana Islands", "Ohio", "Oklahoma",
          "Oregon", "Palau", "Pennsylvania", "Puerto Rico", "Rhode Island",
          "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
          "Vermont", "U.S. Virgin Islands", "Virginia", "Washington",
          "West Virginia", "Wisconsin", "Wyoming"]

BASIC_STAT_NAMES = ["mp", "fg", "fga", "fg_pct", "tp", "tpa", "tp_pct", "ft",
                    "fta", "ft_pct", "orb", "drb", "trb", "ast", "stl", "blk", 
                    "tov", "pf", "pts"]
ADVANCED_STAT_NAMES = ["ts", "efg", "tpar", "ftr", "orb_pct", "drb_pct",
                       "trb_pct", "ast_pct", "stl_pct", "blk_pct", "tov_pct", 
                       "usg_rate", "ortg", "drtg"]

PLAYER_STAT_NAMES = ["started", "plus_minus"]


# def calcluate_team_posessions(stats):
    # possession_formula: 0.5 * ((Tm FGA + 0.4 * Tm FTA - 1.07 * (Tm ORB / (Tm ORB + Opp DRB)) * (Tm FGA - Tm FG) + Tm TOV) + (Opp FGA + 0.4 * Opp FTA - 1.07 * (Opp ORB / (Opp ORB + Tm DRB)) * (Opp FGA - Opp FG) + Opp TOV))


def get_datetime(datetime_str):
    est = pytz.timezone("America/New_York")
    date = parse(datetime_str)
    date = est.localize(date)
    return date


def update_auto_increments():
    output = StringIO()
    django.core.management.call_command(
        "sqlsequencereset", "stats", stdout=output, no_color=True)
    connection = None
    try:
        connection = psycopg2.connect(connection_url, sslmode='require')
        cursor = connection.cursor()
        cursor.execute(output.getvalue())
        cursor.close()
        connection.commit()
    except psycopg2.DatabaseError as e:
        if connection:
            connection.rollback()
            print("rolling back...")
        print(f"Error {e}")
        sys.exit(1)
    finally:
        if connection:
            connection.close()

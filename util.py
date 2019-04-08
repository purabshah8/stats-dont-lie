import sys
import django
import psycopg2
import pytz
from dateutil.parser import parse
from django.utils.six import StringIO

aba_teams = ["Nets", "Spurs", "Pacers", "Nuggets"]
states = ["Alabama", "Alaska", "American Samoa", "Arizona", "Arkansas",
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
        connection = psycopg2.connect(
            "dbname=nba user=purab password=godricshallows")
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

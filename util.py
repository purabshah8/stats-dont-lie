import sys, django, psycopg2, pytz
from dateutil.parser import parse
from django.utils.six import StringIO

aba_teams = ["Nets", "Spurs", "Pacers", "Nuggets"]


def get_datetime(datetime_str):
    est = pytz.timezone('America/New_York')
    date = parse(datetime_str)
    date = est.localize(date)
    return date

def update_auto_increments():
    output = StringIO()
    django.core.management.call_command('sqlsequencereset', 'stats', stdout=output, no_color=True)
    connection = None
    try:
        connection = psycopg2.connect("dbname=nba user=purab password=godricshallows")
        cursor = connection.cursor()
        cursor.execute(output.getvalue())
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

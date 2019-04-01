from django.db import models

class League(models.Model):
    name = models.CharField(max_length=8)
    year_founded = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'league'


class Conference(models.Model):
    name = models.CharField(max_length=32)
    abbreviation = models.CharField(max_length=8)
    league = models.ForeignKey('League', models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'conference'


class Division(models.Model):
    name = models.CharField(max_length=32)
    abbreviation = models.CharField(max_length=8)
    conference = models.ForeignKey(Conference, models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'division'


class Location(models.Model):
    precision = models.CharField(max_length=16)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    state = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=64)
    postal_code = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.precision == 'country':
            return self.country
        if self.precision == 'city':
            loc = self.city
            if self.state:
                loc += ", " + self.state
            return loc + ", " + self.country
        if self.precision == 'address': 
            address =  self.address
            if self.city:
                address += ", " + self.city
            if self.state:
                address += ", " + self.state
            if self.postal_code:
                address += " " + str(self.postal_code)
            if self.country and self.country != 'USA':
                address += " " + self.country
            return address

    class Meta:
        db_table = 'location'


class Arena(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    location = models.ForeignKey('Location', models.DO_NOTHING)
    capacity = models.IntegerField()
    year_opened = models.IntegerField()
    year_closed = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'arena'


class Team(models.Model):
    division = models.ForeignKey(Division, models.DO_NOTHING)
    name = models.CharField(max_length=16)
    city = models.CharField(max_length=16)
    arena = models.ForeignKey(Arena, models.DO_NOTHING)
    year_founded = models.IntegerField()
    abbreviation = models.CharField(max_length=8)

    def __str__(self):
        return self.city + " " + self.name
    class Meta:
        db_table = 'team'


class Season(models.Model):
    league = models.ForeignKey(League, models.DO_NOTHING)
    year = models.IntegerField()
    season_start = models.DateField(blank=True, null=True)
    playoff_start = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.league.name.upper() + " " + str(self.year)

    class Meta:
        db_table = 'season'


class Person(models.Model):
    last_name = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32, blank=True, null=True)
    preferred_name = models.CharField(max_length=32, blank=True, null=True)
    dob = models.DateField()
    college = models.CharField(max_length=64, blank=True, null=True)
    birthplace = models.ForeignKey(Location, models.DO_NOTHING)

    def __str__(self):
        return self.preferred_name + " " + self.last_name
    class Meta:
        db_table = 'person'


class Referee(models.Model):
    id = models.OneToOneField(Person, models.DO_NOTHING, db_column='id', primary_key=True)
    jersey_number = models.IntegerField()
    rookie_season = models.ForeignKey('Season', models.DO_NOTHING)

    def __str__(self):
        return self.id.__str__()
        
    class Meta:
        db_table = 'referee'


class TeamEmployee(models.Model):
    id = models.OneToOneField(Person, models.DO_NOTHING, db_column='id', primary_key=True)
    team = models.ForeignKey(Team, models.DO_NOTHING)
    role = models.CharField(max_length=16)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.id.__str__()

    class Meta:
        db_table = 'team_employee'


class Player(models.Model):
    id = models.OneToOneField(Person, models.DO_NOTHING, db_column='id', primary_key=True)
    height = models.IntegerField()
    weight = models.IntegerField()
    shooting_hand = models.CharField(max_length=5)
    rookie_season = models.ForeignKey('Season', models.DO_NOTHING, related_name="rookie_season")
    final_season = models.ForeignKey('Season', models.DO_NOTHING, related_name="final_season", null=True)
    image_url = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.id.__str__()

    class Meta:
        db_table = 'player'


class Position(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16)
    abbreviation = models.CharField(max_length=2)

    def __str__(self):
        return self.abbreviation

    class Meta:
        db_table = 'position'


class PlayerPosition(models.Model):
    player = models.ForeignKey(Player, models.DO_NOTHING)
    position = models.ForeignKey('Position', models.DO_NOTHING)

    class Meta:
        db_table = 'player_position'

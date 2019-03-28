# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class League(models.Model):
    name = models.CharField(max_length=8)
    year_founded = models.IntegerField()

    class Meta:
        db_table = 'league'


class Conference(models.Model):
    name = models.CharField(max_length=32)
    abbreviation = models.CharField(max_length=8)
    league = models.ForeignKey('League', models.DO_NOTHING)

    class Meta:
        db_table = 'conference'


class Division(models.Model):
    name = models.CharField(max_length=32)
    abbreviation = models.CharField(max_length=8)
    conference = models.ForeignKey(Conference, models.DO_NOTHING)

    class Meta:
        db_table = 'division'


class Location(models.Model):
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    state = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=64)
    postal_code = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'location'


class Arena(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    location = models.ForeignKey('Location', models.DO_NOTHING)
    capacity = models.IntegerField()
    year_opened = models.IntegerField()
    year_closed = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'arena'


class Team(models.Model):
    division = models.ForeignKey(Division, models.DO_NOTHING)
    name = models.CharField(max_length=16)
    city = models.CharField(max_length=16)
    arena = models.ForeignKey(Arena, models.DO_NOTHING)
    year_founded = models.IntegerField()
    abbreviation = models.CharField(max_length=8)

    class Meta:
        db_table = 'team'


class Season(models.Model):
    league = models.ForeignKey(League, models.DO_NOTHING)
    year = models.IntegerField()
    preseason_start = models.DateField(blank=True, null=True)
    season_start = models.DateField(blank=True, null=True)
    playoff_start = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'season'


class Person(models.Model):
    last_name = models.CharField(max_length=16)
    first_name = models.CharField(max_length=16)
    middle_name = models.CharField(max_length=16, blank=True, null=True)
    preferred_name = models.CharField(max_length=16, blank=True, null=True)
    dob = models.DateField()
    college = models.CharField(max_length=32, blank=True, null=True)
    birthplace = models.ForeignKey(Location, models.DO_NOTHING)

    class Meta:
        db_table = 'person'


class Referee(models.Model):
    id = models.ForeignKey(Person, models.DO_NOTHING, db_column='id', primary_key=True)
    jersey_number = models.IntegerField()
    rookie_season = models.ForeignKey('Season', models.DO_NOTHING)

    class Meta:
        db_table = 'referee'


class TeamEmployee(models.Model):
    id = models.ForeignKey(Person, models.DO_NOTHING, db_column='id', primary_key=True)
    team = models.ForeignKey(Team, models.DO_NOTHING)
    role = models.CharField(max_length=16)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'team_employee'


class Player(models.Model):
    id = models.ForeignKey(Person, models.DO_NOTHING, db_column='id', primary_key=True)
    height = models.IntegerField()
    weight = models.IntegerField()
    shooting_hand = models.CharField(max_length=5)
    rookie_season = models.ForeignKey('Season', models.DO_NOTHING)
    final_season = models.ForeignKey('Season', models.DO_NOTHING)
    image_url = models.CharField(max_length=128)

    class Meta:
        db_table = 'player'


class Position(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16)
    abbreviation = models.CharField(max_length=2)

    class Meta:
        db_table = 'position'


class PlayerPosition(models.Model):
    player = models.ForeignKey(Player, models.DO_NOTHING)
    position = models.ForeignKey('Position', models.DO_NOTHING)

    class Meta:
        db_table = 'player_position'

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Arena(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    location = models.ForeignKey('Location', models.DO_NOTHING)
    capacity = models.IntegerField()
    year_opened = models.IntegerField()
    year_closed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'arena'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Conference(models.Model):
    name = models.CharField(max_length=32)
    abbreviation = models.CharField(max_length=8)
    league = models.ForeignKey('League', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'conference'


class Division(models.Model):
    name = models.CharField(max_length=32)
    abbreviation = models.CharField(max_length=8)
    conference = models.ForeignKey(Conference, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'division'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Game(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    home = models.ForeignKey('Team', models.DO_NOTHING)
    away = models.ForeignKey('Team', models.DO_NOTHING)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    winner = models.ForeignKey('Team', models.DO_NOTHING)
    ref_one = models.ForeignKey('Person', models.DO_NOTHING, blank=True, null=True)
    ref_two = models.ForeignKey('Person', models.DO_NOTHING, blank=True, null=True)
    ref_three = models.ForeignKey('Person', models.DO_NOTHING, blank=True, null=True)
    tipoff = models.DateTimeField(blank=True, null=True)
    attendance = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game'


class GamePeriod(models.Model):
    game = models.ForeignKey(Game, models.DO_NOTHING, primary_key=True)
    number = models.IntegerField()
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'game_period'
        unique_together = (('game', 'number'),)


class League(models.Model):
    name = models.CharField(max_length=8)
    year_founded = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'league'


class Location(models.Model):
    precision = models.CharField(max_length=32)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    state = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=64)
    postal_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'


class Person(models.Model):
    last_name = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32, blank=True, null=True)
    preferred_name = models.CharField(max_length=32, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    college = models.TextField(blank=True, null=True)
    birthplace = models.ForeignKey(Location, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'


class Player(models.Model):
    person = models.ForeignKey(Person, models.DO_NOTHING, primary_key=True)
    height = models.IntegerField()
    weight = models.IntegerField()
    shooting_hand = models.CharField(max_length=5)
    rookie_season = models.ForeignKey('Season', models.DO_NOTHING)
    final_season = models.ForeignKey('Season', models.DO_NOTHING, blank=True, null=True)
    image_url = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player'


class PlayerPosition(models.Model):
    player = models.ForeignKey(Person, models.DO_NOTHING)
    position = models.ForeignKey('Position', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'player_position'


class PlayerStatline(models.Model):
    statline = models.ForeignKey('Statline', models.DO_NOTHING, primary_key=True)
    player = models.ForeignKey(Person, models.DO_NOTHING)
    started = models.BooleanField()
    plus_minus = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'player_statline'


class PlayerTeamSeason(models.Model):
    player = models.ForeignKey(Person, models.DO_NOTHING)
    team_season = models.ForeignKey('TeamSeason', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'player_team_season'


class Position(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16)
    abbreviation = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'position'


class Referee(models.Model):
    person = models.ForeignKey(Person, models.DO_NOTHING, primary_key=True)
    jersey_number = models.IntegerField(blank=True, null=True)
    rookie_season = models.ForeignKey('Season', models.DO_NOTHING)
    final_season = models.ForeignKey('Season', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referee'


class Season(models.Model):
    league = models.ForeignKey(League, models.DO_NOTHING)
    year = models.IntegerField()
    start_date = models.DateTimeField(blank=True, null=True)
    playoffs_start_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'season'


class Statline(models.Model):
    game = models.ForeignKey(Game, models.DO_NOTHING)
    team = models.ForeignKey('Team', models.DO_NOTHING)
    mp = models.IntegerField(blank=True, null=True)
    fg = models.IntegerField(blank=True, null=True)
    fga = models.IntegerField(blank=True, null=True)
    fg_pct = models.FloatField(blank=True, null=True)
    tp = models.IntegerField(blank=True, null=True)
    tpa = models.IntegerField(blank=True, null=True)
    tp_pct = models.FloatField(blank=True, null=True)
    ft = models.IntegerField(blank=True, null=True)
    fta = models.IntegerField(blank=True, null=True)
    ft_pct = models.FloatField(blank=True, null=True)
    orb = models.IntegerField(blank=True, null=True)
    drb = models.IntegerField(blank=True, null=True)
    trb = models.IntegerField(blank=True, null=True)
    ast = models.IntegerField(blank=True, null=True)
    stl = models.IntegerField(blank=True, null=True)
    blk = models.IntegerField(blank=True, null=True)
    tov = models.IntegerField(blank=True, null=True)
    pf = models.IntegerField(blank=True, null=True)
    pts = models.IntegerField(blank=True, null=True)
    poss = models.FloatField(blank=True, null=True)
    ts = models.FloatField(blank=True, null=True)
    efg = models.FloatField(blank=True, null=True)
    tpar = models.FloatField(blank=True, null=True)
    ftr = models.FloatField(blank=True, null=True)
    orb_pct = models.FloatField(blank=True, null=True)
    drb_pct = models.FloatField(blank=True, null=True)
    trb_pct = models.FloatField(blank=True, null=True)
    ast_pct = models.FloatField(blank=True, null=True)
    stl_pct = models.FloatField(blank=True, null=True)
    blk_pct = models.FloatField(blank=True, null=True)
    tov_pct = models.FloatField(blank=True, null=True)
    usg_rate = models.FloatField(blank=True, null=True)
    ortg = models.FloatField(blank=True, null=True)
    drtg = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statline'


class Team(models.Model):
    division = models.ForeignKey(Division, models.DO_NOTHING)
    name = models.CharField(max_length=16)
    city = models.CharField(max_length=16)
    arena = models.ForeignKey(Arena, models.DO_NOTHING)
    year_founded = models.IntegerField()
    year_defunct = models.IntegerField(blank=True, null=True)
    abbreviation = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'team'


class TeamEmployee(models.Model):
    person = models.ForeignKey(Person, models.DO_NOTHING, primary_key=True)
    team = models.ForeignKey(Team, models.DO_NOTHING)
    role = models.CharField(max_length=16)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team_employee'


class TeamSeason(models.Model):
    team = models.ForeignKey(Team, models.DO_NOTHING)
    season = models.ForeignKey(Season, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'team_season'

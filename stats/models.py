from django.db import models
from util import aba_teams

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

    def get_season(self, year):
        league_id = 2 if self.name in aba_teams and year < 1977 else 1
        return TeamSeason(team_id=self.id, season_id=Season.objects.get(year=year, league_id=league_id).id)
    
    @classmethod
    def find(cls,team_name):
        city, nickname = team_name.split(" ")
        return cls.objects.get(city=city, name=nickname)

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
    dob = models.DateField(blank=True, null=True)
    college = models.TextField(blank=True, null=True)
    birthplace = models.ForeignKey(Location, models.DO_NOTHING)

    def __str__(self):
        return self.preferred_name + " " + self.last_name
    class Meta:
        db_table = 'person'

    @classmethod
    def find(cls, full_name):
        preferred_name, last_name = full_name.split(" ")
        return cls.objects.get(preferred_name=preferred_name, last_name=last_name)


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


class TeamSeason(models.Model):
    team = models.ForeignKey(Team, models.DO_NOTHING)
    season = models.ForeignKey(Season, models.DO_NOTHING)

    def __str__(self):
        return self.team.name + " " + str(self.season.year)
    class Meta:
        db_table = 'team_season'


class PlayerTeamSeason(models.Model):
    player = models.ForeignKey(Player, models.DO_NOTHING)
    team_season = models.ForeignKey('TeamSeason', models.DO_NOTHING)

    class Meta:
        db_table = 'player_team_season'

class Game(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    home = models.ForeignKey('Team', models.DO_NOTHING, related_name="home_team")
    away = models.ForeignKey('Team', models.DO_NOTHING, related_name="away_team")
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    winner = models.ForeignKey('Team', models.DO_NOTHING, related_name="winner")
    ref_one = models.ForeignKey('Referee', models.DO_NOTHING, blank=True, null=True, related_name="first_ref")
    ref_two = models.ForeignKey('Referee', models.DO_NOTHING, blank=True, null=True, related_name="second_ref")
    ref_three = models.ForeignKey('Referee', models.DO_NOTHING, blank=True, null=True, related_name="third_ref")
    tipoff = models.DateTimeField(blank=True, null=True)
    attendance = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        self.id
    class Meta:
        db_table = 'game'


class GamePeriod(models.Model):
    game = models.ForeignKey(Game, models.DO_NOTHING)
    number = models.IntegerField()
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    class Meta:
        db_table = 'game_period'


class Statline(models.Model):
    game = models.ForeignKey(Game, models.DO_NOTHING)
    team = models.ForeignKey('Team', models.DO_NOTHING)
    mp = models.IntegerField(blank=True, null=True)
    fg = models.IntegerField()
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
    pts = models.IntegerField()

    class Meta:
        db_table = 'statline'


class AdvancedStatline(models.Model):
    id = models.OneToOneField('Statline', models.DO_NOTHING, db_column='id', primary_key=True)
    ts = models.FloatField(blank=True, null=True)
    efg = models.FloatField(blank=True, null=True)
    tpar = models.FloatField(blank=True, null=True)
    ftr = models.FloatField(blank=True, null=True)
    orb_pct = models.FloatField()
    drb_pct = models.FloatField()
    trb_pct = models.FloatField()
    ast_pct = models.FloatField()
    stl_pct = models.FloatField()
    blk_pct = models.FloatField()
    tov_pct = models.FloatField(blank=True, null=True)
    usg_rate = models.FloatField()
    ortg = models.IntegerField()
    drtg = models.IntegerField()

    class Meta:
        db_table = 'advanced_statline'


class PlayerStatline(models.Model):
    id = models.OneToOneField('Statline', models.DO_NOTHING, db_column='id', primary_key=True)
    player = models.ForeignKey(Player, models.DO_NOTHING)
    started = models.BooleanField(blank=True, null=True)
    plus_minus = models.IntegerField()

    class Meta:
        db_table = 'player_statline'
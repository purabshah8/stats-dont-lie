import re
from django.db import models
from django.db.models import Sum, Avg
from util import ABA_TEAMS, BASIC_STAT_NAMES, ADVANCED_STAT_NAMES, PLAYER_STAT_NAMES
from datetime import date
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


# %load_ext autoreload
# %autoreload 2
# from stats.models import *

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
        league_id = 2 if self.name in ABA_TEAMS and year < 1977 else 1
        season = Season.objects.get(year=year, league_id=league_id)
        return TeamSeason.objects.get(team_id=self.id, season_id=season.id)
    
    def get_roster(self,year):
        team_season = self.get_season(year)
        return list(PlayerTeamSeason.objects.filter(team_season=team_season))

    @classmethod
    def find(cls,team_name):
        name = team_name.split(" ")
        if "Blazers" in name:
            city = name[0]
            nickname = " ".join(name[1:])
        else:
            city = " ".join(name[:-1])
            nickname = name[-1]
        try:
            return cls.objects.get(city=city, name=nickname)
        except:
            print("Multiple Teams Found")
            breakpoint()
            return


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
        return self.get_name()

    class Meta:
        db_table = 'person'

    def get_name(self):
        return self.preferred_name + " " + self.last_name

    @classmethod
    def find(cls, full_name, year=None):
        names = full_name.split(" ")
        if len(names) == 2:
            preferred_name, last_name = names
        elif re.search(r"^[vV][ao]n", names[1]) or full_name == "Luc Mbah a Moute":
            preferred_name = names[0]
            last_name = " ".join(names[1:])
        else:
            preferred_name = " ".join(names[:1])
            last_name = names[-1]
        try:
            return cls.objects.get(preferred_name=preferred_name, last_name=last_name)
        except ObjectDoesNotExist:
            breakpoint()
            print(f"Could not find a match for {full_name}")
        except MultipleObjectsReturned:
            if year:
                active_players = []
                people = cls.objects.filter(preferred_name=preferred_name, last_name=last_name)
                for person in people:
                    player = person.player
                    first_year = player.rookie_season.year
                    if player.final_season is None:
                        last_year = year
                    else:
                        last_year = player.final_season.year
                    is_active = first_year <= year and year <= last_year
                    if is_active:
                        active_players.append(player)
                if len(active_players) == 1:
                    return active_players[0].id
                else:
                    breakpoint()
                    print(f"Found multiple matching players for {full_name}")
                    return
            else:
                breakpoint()
                print(f"Found multiple matches for {full_name}")

            
class Referee(models.Model):
    id = models.OneToOneField(Person, models.DO_NOTHING, db_column='id', primary_key=True)
    jersey_number = models.IntegerField()
    rookie_season = models.ForeignKey('Season', models.DO_NOTHING, related_name="ref_rookie_season")
    final_season = models.ForeignKey('Season', models.DO_NOTHING, related_name="ref_final_season", null=True)

    def __str__(self):
        return self.id.__str__()
        
    class Meta:
        db_table = 'referee'

    def is_active(self, year):
        first_year = self.rookie_season.year
        if self.final_season is None:
            last_year = date.today().year
        else:
            last_year = self.final_season.year
        return first_year <= year and year <= last_year
        

    def get_name(self):
        return self.id.get_name()
    
    @classmethod
    def find(cls, full_name):
        names = full_name.split(" ")
        if len(names) == 2:
            preferred_name, last_name = names
        elif re.search(r"^[vV][ao]n", names[1]):
            preferred_name = names[0]
            last_name = " ".join(names[1:])
        else:
            preferred_name = " ".join(names[:1])
            last_name = names[-1]
        matches = cls.objects.filter(id__preferred_name=preferred_name, id__last_name=last_name)
        return matches


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

    def get_name(self):
        return self.id.get_name()


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

    def get_name(self):
        return self.id.get_name()

    @classmethod
    def find(cls, full_name):
        names = full_name.split(" ")
        if len(names) == 2:
            preferred_name, last_name = names
        elif re.search(r"^[vV][ao]n", names[1]) or full_name == "Luc Mbah a Moute":
            preferred_name = names[0]
            last_name = " ".join(names[1:])
        else:
            preferred_name = " ".join(names[:1])
            last_name = names[-1]
        matches = cls.objects.filter(id__preferred_name=preferred_name, id__last_name=last_name)
        if len(matches) == 1:
            return matches[0]
        elif len(matches) < 1:
            raise ObjectDoesNotExist(f"Could not find a match for Player {full_name}")
        else:
            print(f"Found multiple matches for Player {full_name}")
            breakpoint()
            return


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

    def get_regular_statlines(self):
        return Statline.objects.filter(team=self.team, 
            playerstatline__isnull=True, 
            game__tipoff__lt=self.season.playoff_start, 
            game__tipoff__gte=self.season.season_start)

    def get_playoff_statlines(self):
        return Statline.objects.filter(team=self.team, 
            playerstatline__isnull=True, 
            game__tipoff__gte=self.season.playoff_start, 
            game__tipoff__lt=date(self.season.year, 7, 1))
    
    def get_raw_stats(self):
        raw_stats = {}
        team_stats = self.get_regular_statlines()
        for stat in BASIC_STAT_NAMES:
            stat_values = team_stats.values_list(stat, flat=True)
            raw_stats[stat] = list(stat_values)
        return raw_stats

    def get_season_totals(self):
        team_stats = self.get_regular_statlines()
        totals = team_stats.aggregate(mp=Sum("mp"), fg=Sum("fg"), 
            fga=Sum("fga"), tp=Sum("tp"), tpa=Sum("tpa"), 
            ft=Sum("ft"), fta=Sum("fta"), orb=Sum("orb"), 
            drb=Sum("drb"), trb=Sum("trb"), ast=Sum("ast"), 
            stl=Sum("stl"), blk=Sum("blk"), tov=Sum("tov"), 
            pf=Sum("pf"), pts=Sum("pts"))
        totals["fg_pct"] = totals["fg"] / totals["fga"]
        totals["tp_pct"] = totals["tp"] / totals["tpa"]
        totals["ft_pct"] = totals["ft"] / totals["fta"]
        return totals
    class Meta:
        db_table = 'team_season'


class PlayerTeamSeason(models.Model):
    player = models.ForeignKey(Player, models.DO_NOTHING)
    team_season = models.ForeignKey('TeamSeason', models.DO_NOTHING)

    def __str__(self):
        return self.player.get_name() + " " + self.team_season.__str__()

    def get_regular_statlines(self):
        return Statline.objects.filter(playerstatline__isnull=False,
            playerstatline__player=self.player.id.id, 
            game__tipoff__lt=self.team_season.season.playoff_start, 
            game__tipoff__gte=self.team_season.season.season_start)

    def get_playoff_statlines(self):
        return Statline.objects.filter(playerstatline__isnull=False,
            playerstatline__player=self.player.id.id, 
            game__tipoff__gte=self.team_season.season.playoff_start, 
            game__tipoff__lt=date(self.team_season.season.year, 7, 1))
    
    def get_raw_stats(self):
        raw_stats = {}
        player_stats = self.get_regular_statlines()
        for stat in BASIC_STAT_NAMES:
            stat_values = player_stats.values_list(stat, flat=True)
            raw_stats[stat] = list(stat_values)
        for stat in PLAYER_STAT_NAMES:
            stat_values = player_stats.values_list("playerstatline__"+stat, flat=True)
            raw_stats[stat] = list(stat_values)
        return raw_stats

    def get_season_totals(self):
        team_stats = self.get_regular_statlines()
        totals = team_stats.aggregate(mp=Sum("mp"), fg=Sum("fg"), 
            fga=Sum("fga"), tp=Sum("tp"), tpa=Sum("tpa"), 
            ft=Sum("ft"), fta=Sum("fta"), orb=Sum("orb"), 
            drb=Sum("drb"), trb=Sum("trb"), ast=Sum("ast"), 
            stl=Sum("stl"), blk=Sum("blk"), tov=Sum("tov"), 
            pf=Sum("pf"), pts=Sum("pts"))
        totals["fg_pct"] = totals["fg"] / totals["fga"]
        totals["tp_pct"] = totals["tp"] / totals["tpa"]
        totals["ft_pct"] = totals["ft"] / totals["fta"]
        starts = 0
        plus_minus = 0
        for stat in team_stats:
            plus_minus += stat.playerstatline.plus_minus
            if stat.playerstatline.started:
                starts += 1
        totals["plus_minus"] = plus_minus
        totals["starts"] = starts
        return totals
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
        return self.id
    
    class Meta:
        db_table = 'game'

    def get_stats(self, team):
        if team == "home":
            return Statline.objects.filter(team=self.home, game=self.id)
        else:
            return Statline.objects.filter(team=self.away, game=self.id)



class GamePeriod(models.Model):
    game = models.ForeignKey(Game, models.DO_NOTHING)
    number = models.IntegerField()
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    def __str__(self):
        return self.game.id + " Q" + str(self.number)

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

    def __str__(self):
        return self.game.id + " " + self.team.abbreviation + str(self.id)
    
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
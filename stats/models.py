from django.db import models
from django.db.models import Sum, Avg, Q, StdDev
from django.db.models.functions import Greatest  
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity

import re
from datetime import date
from util import ABA_TEAMS, STAT_NAMES, PLAYER_STAT_NAMES

# %load_ext autoreload
# %autoreload 2
# from stats.models import *
# from django.db.models import Q
# nets = Team.find("Brooklyn Nets")
# nets19 = nets.get_season(2019)
# dlo = Player.find("D'Angelo Russell")
# dlo19 = PlayerTeamSeason.objects.get(player=dlo, team_season=nets19)

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
            address = self.address
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

    def get_roster(self, year):
        team_season = self.get_season(year)
        return list(PlayerTeamSeason.objects.filter(team_season=team_season))

    @classmethod
    def find(cls, team_name):
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
    start_date = models.DateTimeField(blank=True, null=True)
    playoffs_start_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.league.name.upper() + " " + str(self.year)

    def get_aggregate_stats(self):
        all_statlines = Statline.objects.filter(
            playerstatline__isnull=False,
            game__tipoff__lt=self.playoffs_start_date,
            game__tipoff__gte=self.start_date)

        averages = all_statlines.aggregate(
            mp=Avg("mp"), fg=Avg("fg"), fga=Avg("fga"), fg_pct=Avg("fg_pct"), 
            tp=Avg("tp"), tpa=Avg("tpa"), tp_pct=Avg("tp_pct"), ft=Avg("ft"), 
            fta=Avg("fta"), ft_pct=Avg("ft_pct"), orb=Avg("orb"), 
            drb=Avg("drb"), trb=Avg("trb"), ast=Avg("ast"), stl=Avg("stl"),
            blk=Avg("blk"), tov=Avg("tov"), pf=Avg("pf"), pts=Avg("pts"), 
            poss=Avg("poss"), ts=Avg("ts"), efg=Avg("efg"), tpar=Avg("tpar"), 
            ftr=Avg("ftr"), orb_pct=Avg("orb_pct"), drb_pct=Avg("drb_pct"),
            trb_pct=Avg("trb_pct"), ast_pct=Avg("ast_pct"),
            stl_pct=Avg("stl_pct"), blk_pct=Avg("blk_pct"),
            tov_pct=Avg("tov_pct"), usg_rate=Avg("usg_rate"),
            ortg=Avg("ortg"), drtg=Avg("drtg"),
            plus_minus=Avg("playerstatline__plus_minus"))

        std_devs = all_statlines.aggregate(
            mp=StdDev("mp"), fg=StdDev("fg"), fga=StdDev("fga"), 
            fg_pct=StdDev("fg_pct"), tp=StdDev("tp"), tpa=StdDev("tpa"), 
            tp_pct=StdDev("tp_pct"), ft=StdDev("ft"),fta=StdDev("fta"), 
            ft_pct=StdDev("ft_pct"), orb=StdDev("orb"), drb=StdDev("drb"),
            trb=StdDev("trb"), ast=StdDev("ast"), stl=StdDev("stl"),
            blk=StdDev("blk"), tov=StdDev("tov"), pf=StdDev("pf"),
            pts=StdDev("pts"), plus_minus=StdDev("playerstatline__plus_minus"),
            poss=StdDev("poss"), ts=StdDev("ts"), efg=StdDev("efg"),
            tpar=StdDev("tpar"), ftr=StdDev("ftr"), orb_pct=StdDev("orb_pct"),
            drb_pct=StdDev("drb_pct"), trb_pct=StdDev("trb_pct"),
            ast_pct=StdDev("ast_pct"), stl_pct=StdDev("stl_pct"),
            blk_pct=StdDev("blk_pct"), tov_pct=StdDev("tov_pct"),
            usg_rate=StdDev("usg_rate"), ortg=StdDev("ortg"), drtg=StdDev("drtg"))
        
        return { "averages" : averages, "standard_deviations": std_devs }

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
    def search(cls, query_str):
        return cls.objects.annotate(
            similarity=Greatest(
                TrigramSimilarity('first_name', query_str), 
                TrigramSimilarity('last_name', query_str), 
                TrigramSimilarity('preferred_name', query_str))
            ).filter(similarity__gte=0.4).order_by('-similarity') 
        

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
                people = cls.objects.filter(
                    preferred_name=preferred_name, last_name=last_name)
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
                    return active_players[0].person
                else:
                    breakpoint()
                    print(f"Found multiple matching players for {full_name}")
                    return
            else:
                breakpoint()
                print(f"Found multiple matches for {full_name}")


class Referee(models.Model):
    person = models.OneToOneField(Person, models.DO_NOTHING, primary_key=True)
    jersey_number = models.IntegerField(blank=True, null=True)
    rookie_season = models.ForeignKey(
        'Season', models.DO_NOTHING, related_name="ref_rookie_season")
    final_season = models.ForeignKey(
        'Season', models.DO_NOTHING, related_name="ref_final_season", null=True)

    def __str__(self):
        return self.person.__str__()

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
        return self.person.get_name()

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
        matches = cls.objects.filter(
            person__preferred_name=preferred_name, person__last_name=last_name)
        return matches


class TeamEmployee(models.Model):
    person = models.OneToOneField(Person, models.DO_NOTHING, primary_key=True)
    team = models.ForeignKey(Team, models.DO_NOTHING)
    role = models.CharField(max_length=16)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.person.__str__()

    class Meta:
        db_table = 'team_employee'

    def get_name(self):
        return self.person.get_name()


class Player(models.Model):
    person = models.OneToOneField(Person, models.DO_NOTHING, primary_key=True)
    height = models.IntegerField()
    weight = models.IntegerField()
    shooting_hand = models.CharField(max_length=5)
    rookie_season = models.ForeignKey(
        'Season', models.DO_NOTHING, related_name="rookie_season")
    final_season = models.ForeignKey(
        'Season', models.DO_NOTHING, related_name="final_season", null=True)
    image_url = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.person.__str__()

    # def get_career_totals(self):
    #     career_totals = {}
    #     player_seasons = PlayerTeamSeason.objects.filter(player=self)
    #     for player_season in player_seasons:
    #         total_stats = player_season.get_season_totals()
    #         for stat, values in total_stats:
    #             if stat in career_totals:
    #                 career_totals[stat] += values
    #             else:
    #                 career_totals[stat] = values
    #     breakpoint()
    #     return career_totals
    class Meta:
        db_table = 'player'

    def get_name(self):
        return self.person.get_name()


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
        matches = cls.objects.filter(
            person__preferred_name=preferred_name, person__last_name=last_name)
        if len(matches) == 1:
            return matches[0]
        elif len(matches) < 1:
            raise ObjectDoesNotExist(
                f"Could not find a match for Player {full_name}")
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

    def get_games(self):
        return Game.objects.filter(
            Q(home=self.team) | Q(away=self.team),
            tipoff__lt=self.season.playoffs_start_date,
            tipoff__gte=self.season.start_date)

    def get_statlines(self):
        return Statline.objects.filter(
            team=self.team,
            playerstatline__isnull=True,
            game__tipoff__lt=self.season.playoffs_start_date,
            game__tipoff__gte=self.season.start_date).order_by('game__tipoff')

    def get_opp_statlines(self):
        return Statline.objects.filter(
            Q(game__home=self.team) | Q(game__away=self.team),
            game__tipoff__lt=self.season.playoffs_start_date,
            game__tipoff__gte=self.season.start_date,
            playerstatline__isnull=True
            ).exclude(team=self.team).order_by('game__tipoff')


    def get_playoff_statlines(self):
        return Statline.objects.filter(
            team=self.team,
            playerstatline__isnull=True,
            game__tipoff__gte=self.season.playoffs_start_date,
            game__tipoff__lt=date(self.season.year, 7, 1)).order_by('game__tipoff')

    def get_raw_stats(self):
        raw_stats = {}
        # games = self.get_games()
        team_stats = self.get_statlines()
        breakpoint()

        for stat in STAT_NAMES:
            stat_values = team_stats.values_list(stat, flat=True)
            raw_stats[stat] = list(stat_values)
        
        raw_stats["game_dates"] = list(team_stats.values_list("game__tipoff", flat=True))
        opp_stats = self.get_opp_statlines()
        opp_poss = opp_stats.values_list('poss', flat=True)
        # team_poss = team_stats.values_list('poss', flat=True)
        def calc_pace(stats, opp_poss):
            return 48 * ((stats.poss + opp_poss) / (2*(stats.mp/(5*60))))

        raw_stats["pace"] = [ calc_pace(team, opp) for team, opp in zip(team_stats, opp_poss) ]
        # possessions = []
        # pace = []
        # for game in games:
        #     poss = game.get_poss(
        #         "home") if game.home == self.team else game.get_poss("away")
        #     possessions.append(poss)
        #     pace.append(game.get_pace())
        # raw_stats["possessions"] = possessions
        # raw_stats["pace"] = pace
        return raw_stats

    def get_season_totals(self):
        team_stats = self.get_statlines()
        totals = team_stats.aggregate(
            mp=Sum("mp"), fg=Sum("fg"), fga=Sum("fga"),
            tp=Sum("tp"), tpa=Sum("tpa"), ft=Sum("ft"),
            fta=Sum("fta"), orb=Sum("orb"), drb=Sum("drb"),
            trb=Sum("trb"), ast=Sum("ast"), stl=Sum("stl"),
            blk=Sum("blk"), tov=Sum("tov"), pf=Sum("pf"),
            pts=Sum("pts"), poss=Sum("poss"))
        totals["fg_pct"] = totals["fg"] / totals["fga"]
        totals["tp_pct"] = totals["tp"] / totals["tpa"]
        totals["ft_pct"] = totals["ft"] / totals["fta"]
        opp_stats = self.get_opp_statlines()
        opp_totals = opp_stats.aggregate(
            # mp=Sum("mp"), fg=Sum("fg"), fga=Sum("fga"),
            # tp=Sum("tp"), tpa=Sum("tpa"), ft=Sum("ft"),
            # fta=Sum("fta"), orb=Sum("orb"), drb=Sum("drb"),
            # trb=Sum("trb"), ast=Sum("ast"), stl=Sum("stl"),
            # blk=Sum("blk"), tov=Sum("tov"), pf=Sum("pf"),
            pts=Sum("pts"), poss=Sum("poss"))
        totals["gp"] = len(team_stats)
        totals["ts"] = totals["pts"] / (2*(totals["fga"]+0.44*totals["fta"]))
        totals["efg"] = (totals["fg"]+0.5*totals["tpa"]) / totals["fga"]
        totals["tpar"] = totals["tpa"] / totals["fga"]
        totals["ftr"] = totals["fta"] / totals["fga"]
        totals["tov_pct"] = totals["tov"] / totals["poss"] * 100
        totals["blk_pct"] = totals["blk"] / totals["poss"] * 100
        totals["pace"] = totals["poss"] / (totals["mp"]/(60*48*5))
        totals["ortg"] = totals["pts"] / totals["poss"] * 100
        totals["drtg"] = opp_totals["pts"] / opp_totals["poss"] * 100
        totals["plus_minus"] = (totals["pts"] - opp_totals["pts"])/totals["gp"]
        return totals

    class Meta:
        db_table = 'team_season'


class PlayerTeamSeason(models.Model):
    
    player = models.ForeignKey(Player, models.DO_NOTHING)
    team_season = models.ForeignKey('TeamSeason', models.DO_NOTHING)

    class Meta:
        db_table = 'player_team_season'
    
    def __str__(self):
        return self.player.get_name() + " " + self.team_season.__str__()

    def get_statlines(self):
        return Statline.objects.filter(
            playerstatline__isnull=False,
            playerstatline__player=self.player.person.id,
            team=self.team_season.team,
            game__tipoff__lt=self.team_season.season.playoffs_start_date,
            game__tipoff__gte=self.team_season.season.start_date).order_by("game__tipoff")

    def get_playoff_statlines(self):
        return Statline.objects.filter(
            playerstatline__isnull=False,
            playerstatline__player=self.player.person.id,
            game__tipoff__gte=self.team_season.season.playoffs_start_date,
            game__tipoff__lt=date(self.team_season.season.year, 7, 1))

    def get_raw_stats(self):
        raw_stats = {}
        player_stats = self.get_statlines()
        for stat in STAT_NAMES:
            stat_values = player_stats.values_list(stat, flat=True)
            raw_stats[stat] = list(stat_values)
        for stat in PLAYER_STAT_NAMES:
            stat_values = player_stats.values_list(
                "playerstatline__"+stat, flat=True)
            raw_stats[stat] = list(stat_values)
        raw_stats["game_dates"] = list(
            player_stats.values_list("game__tipoff", flat=True))
        return raw_stats

    def get_season_totals(self):
        team_stats = self.get_statlines()
        totals = team_stats.aggregate(
            mp=Sum("mp"), fg=Sum("fg"), fga=Sum("fga"),
            tp=Sum("tp"), tpa=Sum("tpa"), ft=Sum("ft"),
            fta=Sum("fta"), orb=Sum("orb"), drb=Sum("drb"),
            trb=Sum("trb"), ast=Sum("ast"), stl=Sum("stl"),
            blk=Sum("blk"), tov=Sum("tov"), pf=Sum("pf"),
            pts=Sum("pts"))
        try:
            totals["fg_pct"] = totals["fg"] / totals["fga"]
        except ZeroDivisionError:
            totals["fg_pct"] = 0.0
        try:
            totals["tp_pct"] = totals["tp"] / totals["tpa"]
        except ZeroDivisionError:
            totals["tp_pct"] = 0.0
        try:
            totals["ft_pct"] = totals["ft"] / totals["fta"]
        except ZeroDivisionError:
            totals["ft_pct"] = 0.0

        starts = 0
        plus_minus = 0
        for stat in team_stats:
            plus_minus += stat.playerstatline.plus_minus
            if stat.playerstatline.started:
                starts += 1
        totals["plus_minus"] = plus_minus
        totals["starts"] = starts
        totals["gp"] = len(team_stats)
        totals["ts"] = totals["pts"]/(2*(totals["fga"]+0.44*totals["fta"]))
        totals["efg"] = (totals["fg"] + 0.5 * totals["tpa"])/totals["fga"]
        totals["tpar"] = totals["tpa"]/totals["fga"]
        totals["ftr"] = totals["fta"]/totals["fga"]
        return totals



class Game(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    home = models.ForeignKey('Team', models.DO_NOTHING,
                             related_name="home_team")
    away = models.ForeignKey('Team', models.DO_NOTHING,
                             related_name="away_team")
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    winner = models.ForeignKey(
        'Team', models.DO_NOTHING, related_name="winner")
    ref_one = models.ForeignKey(
        'Person', models.DO_NOTHING, 
        blank=True, null=True, 
        related_name="first_ref")
    ref_two = models.ForeignKey(
        'Person', models.DO_NOTHING, 
        blank=True, null=True, 
        related_name="second_ref")
    ref_three = models.ForeignKey(
        'Person', models.DO_NOTHING, 
        blank=True, null=True, 
        related_name="third_ref")
    tipoff = models.DateTimeField(blank=True, null=True)
    attendance = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'game'
        

class GamePeriod(models.Model):
    game = models.ForeignKey(Game, models.DO_NOTHING, primary_key=True)
    number = models.IntegerField()
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    def __str__(self):
        return self.game.id + " Q" + str(self.number)

    class Meta:
        db_table = 'game_period'
        unique_together = (('game', 'number'),)


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
    ortg = models.IntegerField(blank=True, null=True)
    drtg = models.IntegerField(blank=True, null=True)

    def __str__(self):
        # TODO: Change to reflect statline type
        return self.game.id + " " + self.team.abbreviation + str(self.id)

    class Meta:
        db_table = 'statline'

class PlayerStatline(models.Model):
    statline = models.OneToOneField('Statline', models.DO_NOTHING, primary_key=True)
    player = models.ForeignKey(Person, models.DO_NOTHING)
    started = models.BooleanField()
    plus_minus = models.IntegerField()

    class Meta:
        db_table = 'player_statline'

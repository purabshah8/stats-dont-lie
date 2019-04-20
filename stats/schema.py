import graphene

from graphene_django.types import DjangoObjectType
from stats.models import *


class LeagueType(DjangoObjectType):
    class Meta:
        model = League


class ConferenceType(DjangoObjectType):
    class Meta:
        model = Conference


class DivisionType(DjangoObjectType):
    class Meta:
        model = Division


class LocationType(DjangoObjectType):
    class Meta:
        model = Location


class ArenaType(DjangoObjectType):
    class Meta:
        model = Arena


class TeamType(DjangoObjectType):
    class Meta:
        model = Team


class SeasonType(DjangoObjectType):
    class Meta:
        model = Season


class PersonType(DjangoObjectType):
    class Meta:
        model = Person


class RefereeType(DjangoObjectType):
    class Meta:
        model = Referee


class TeamEmployeeType(DjangoObjectType):
    class Meta:
        model = TeamEmployee


class StatlineType(DjangoObjectType):
    class Meta:
        model = Statline


class AdvancedStatlineType(DjangoObjectType):
    class Meta:
        model = AdvancedStatline


class PlayerStatlineType(DjangoObjectType):
    class Meta:
        model = PlayerStatline


class PlayerType(DjangoObjectType):
    person = graphene.Field(PersonType)
    positions = graphene.List(graphene.String)

    class Meta:
        model = Player

    def resolve_person(self, info):
        return self.id

    def resolve_positions(self, info):
        positions = []
        position_queryset = self.playerposition_set.all()
        for playerpos in position_queryset:
            positions.append(playerpos.position.abbreviation)
        return positions


class PositionType(DjangoObjectType):
    class Meta:
        model = Position


class PlayerPositionType(DjangoObjectType):
    class Meta:
        model = PlayerPosition


class PlayerSeasonStatsType(graphene.ObjectType):
    mp = graphene.List(graphene.Int)
    fg = graphene.List(graphene.Int)
    fga = graphene.List(graphene.Int)
    fg_pct = graphene.List(graphene.Float)
    tp = graphene.List(graphene.Int)
    tpa = graphene.List(graphene.Int)
    tp_pct = graphene.List(graphene.Float)
    ft = graphene.List(graphene.Int)
    fta = graphene.List(graphene.Int)
    ft_pct = graphene.List(graphene.Float)
    orb = graphene.List(graphene.Int)
    drb = graphene.List(graphene.Int)
    trb = graphene.List(graphene.Int)
    ast = graphene.List(graphene.Int)
    stl = graphene.List(graphene.Int)
    blk = graphene.List(graphene.Int)
    tov = graphene.List(graphene.Int)
    pf = graphene.List(graphene.Int)
    pts = graphene.List(graphene.Int)
    plus_minus = graphene.List(graphene.Int)
    started = graphene.List(graphene.Boolean)

class PlayerFullStatlineType(graphene.ObjectType):
    mp = graphene.Int()
    fg = graphene.Int()
    fga = graphene.Int()
    fg_pct = graphene.Float()
    tp = graphene.Int()
    tpa = graphene.Int()
    tp_pct = graphene.Float()
    ft = graphene.Int()
    fta = graphene.Int()
    ft_pct = graphene.Float()
    orb = graphene.Int()
    drb = graphene.Int()
    trb = graphene.Int()
    ast = graphene.Int()
    stl = graphene.Int()
    blk = graphene.Int()
    tov = graphene.Int()
    pf = graphene.Int()
    pts = graphene.Int()
    plus_minus = graphene.Int()
    starts = graphene.Int()


class PlayerTeamSeasonType(DjangoObjectType):
    total_stats = graphene.Field(PlayerStatlineType)
    raw_stats = graphene.Field(PlayerSeasonStatsType)

    class Meta:
        model = PlayerTeamSeason

    def resolve_total_stats(self, info):
        self.get_season_totals()

    def resolve_raw_stats(self, info):
        raw_stats = self.get_raw_stats()
        return PlayerSeasonStatsType(**raw_stats)


class TeamStatlineType(graphene.ObjectType):
    mp = graphene.Int()
    fg = graphene.Int()
    fga = graphene.Int()
    fg_pct = graphene.Float()
    tp = graphene.Int()
    tpa = graphene.Int()
    tp_pct = graphene.Float()
    ft = graphene.Int()
    fta = graphene.Int()
    ft_pct = graphene.Float()
    orb = graphene.Int()
    drb = graphene.Int()
    trb = graphene.Int()
    ast = graphene.Int()
    stl = graphene.Int()
    blk = graphene.Int()
    tov = graphene.Int()
    pf = graphene.Int()
    pts = graphene.Int()


class TeamSeasonStatsType(graphene.ObjectType):
    mp = graphene.List(graphene.Int)
    fg = graphene.List(graphene.Int)
    fga = graphene.List(graphene.Int)
    fg_pct = graphene.List(graphene.Float)
    tp = graphene.List(graphene.Int)
    tpa = graphene.List(graphene.Int)
    tp_pct = graphene.List(graphene.Float)
    ft = graphene.List(graphene.Int)
    fta = graphene.List(graphene.Int)
    ft_pct = graphene.List(graphene.Float)
    orb = graphene.List(graphene.Int)
    drb = graphene.List(graphene.Int)
    trb = graphene.List(graphene.Int)
    ast = graphene.List(graphene.Int)
    stl = graphene.List(graphene.Int)
    blk = graphene.List(graphene.Int)
    tov = graphene.List(graphene.Int)
    pf = graphene.List(graphene.Int)
    pts = graphene.List(graphene.Int)


class TeamSeasonType(DjangoObjectType):
    roster = graphene.List(PlayerTeamSeasonType)
    total_stats = graphene.Field(TeamStatlineType)
    raw_stats = graphene.Field(TeamSeasonStatsType)

    class Meta:
        model = TeamSeason

    def resolve_roster(self, info):
        return PlayerTeamSeason.objects.filter(team_season=self)

    def resolve_total_stats(self, info):
        total_stats = self.get_season_totals()
        return TeamStatlineType(**total_stats)

    def resolve_raw_stats(self, info):
        raw_stats = self.get_raw_stats()
        return TeamSeasonStatsType(**raw_stats)


class GameType(DjangoObjectType):
    class Meta:
        model = Game


class GamePeriodType(DjangoObjectType):
    class Meta:
        model = GamePeriod


class RosterType(graphene.ObjectType):
    year = graphene.Int()
    team = graphene.Field(TeamType)
    players = graphene.List(graphene.Field(PlayerType))


class Query(object):
    all_leagues = graphene.List(LeagueType)
    all_conferences = graphene.List(ConferenceType)
    all_divisions = graphene.List(DivisionType)
    all_locations = graphene.List(LocationType)
    all_arenas = graphene.List(ArenaType)
    all_teams = graphene.List(TeamType)
    
    league = graphene.Field(LeagueType, id=graphene.Int(),
                            name=graphene.String())

    conference = graphene.Field(ConferenceType, 
        id=graphene.Int(), name=graphene.String())
    division = graphene.Field(DivisionType, 
        id=graphene.Int(), name=graphene.String())
    location = graphene.Field(LocationType, id=graphene.Int())
    arena = graphene.Field(ArenaType, id=graphene.Int(),
        name=graphene.String())
    team = graphene.Field(TeamType, id=graphene.Int(), 
        name=graphene.String(), city=graphene.String(), 
        abbr=graphene.String())
    person = graphene.Field(PersonType, id=graphene.Int(),
        name=graphene.String())
    player = graphene.Field(PlayerType, id=graphene.Int(), 
        name=graphene.String())
    season = graphene.Field(SeasonType, year=graphene.Int(), 
        league_id=graphene.Int())
    team_season = graphene.Field(TeamSeasonType, 
        team_id=graphene.Int(), year=graphene.Int())
    player_team_season = graphene.Field(PlayerTeamSeasonType, 
        player_id=graphene.Int(), team_season_id=graphene.Int(), 
        team_id=graphene.Int(), year=graphene.Int())
    statlines = graphene.List(StatlineType, 
        game_id=graphene.String())
    player_statlines = graphene.List(PlayerStatlineType, 
        game_id=graphene.String(), player_id=graphene.String())
    advanced_statlines = graphene.List(AdvancedStatlineType, 
        statline_id=graphene.String())
    
    roster = graphene.List(PlayerTeamSeasonType)
    player_season = graphene.List(PlayerTeamSeasonType, player_id=graphene.Int(), year=graphene.Int())

    def resolve_player_team_season(self, info, **kwargs):
        player_id = kwargs.get("player_id")
        team_season_id = kwargs.get("team_season_id")
        team_id = kwargs.get("team_id")
        year = kwargs.get("year")

        if team_season_id is not None:
            return PlayerTeamSeason.objects.get(
                player_id=player_id, team_season_id=team_season_id)
        if team_id is not None and year is not None:
            team_season = TeamSeason.objects.get(team_id=team_id, 
                season__year=year)
            return PlayerTeamSeason.objects.get(player_id=player_id, team_season=team_season)


    def resolve_player_season(self, info, **kwargs):
        player_id = kwargs.get("player_id")
        year = kwargs.get("year")
        return list(PlayerTeamSeason.objects.filter(player_id=player_id, team_season__season__year=year))

    def resolve_team_season(self, info, **kwargs):
        team_id = kwargs.get("team_id")
        year = kwargs.get("year")
        season = Season.objects.get(year=year, league_id=1)
        return TeamSeason.objects.get(team_id=team_id, season=season)

    def resolve_all_teams(self, info, **kwargs):
        return Team.objects.exclude(id=31)

    def resolve_all_leagues(self, info, **kwargs):
        return League.objects.all()

    def resolve_all_conferences(self, info, **kwargs):
        return Conference.objects.all()

    def resolve_all_divisions(self, info, **kwargs):
        return Division.objects.all()

    def resolve_all_locations(self, info, **kwargs):
        return Location.objects.all()

    def resolve_all_arenas(self, info, **kwargs):
        return Arena.objects.all()

    def resolve_league(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id is not None:
            return League.objects.get(pk=id)

        if name is not None:
            return League.objects.get(name=name)

    def resolve_conference(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id is not None:
            return Conference.objects.get(pk=id)

        if name is not None:
            return Conference.objects.get(name=name)

    def resolve_division(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id is not None:
            return Division.objects.get(pk=id)

        if name is not None:
            return Division.objects.get(name=name)

    def resolve_location(self, info, **kwargs):
        id = kwargs.get("id")

        if id is not None:
            return Location.objects.get(pk=id)

    def resolve_arena(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id is not None:
            return Arena.objects.get(pk=id)

        if name is not None:
            return Arena.objects.get(name=name)

    def resolve_team(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")
        abbr = kwargs.get("abbr")

        if id is not None:
            return Team.objects.get(pk=id)

        if name is not None:
            return Team.objects.get(name=name)

        if abbr is not None:
            return Team.objects.get(abbreviation=abbr)

    def resolve_player(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id is not None:
            return Player.objects.get(pk=id)

        if name is not None:
            return Player.find(name)

    def resolve_person(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id is not None:
            return Person.objects.get(pk=id)

        if name is not None:
            return Person.find(name)

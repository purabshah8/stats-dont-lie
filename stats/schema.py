import graphene
from graphene_django.types import DjangoObjectType
from stats.models import *
from django.db.models.functions import Greatest
from django.contrib.postgres.search import TrigramSimilarity

class FullStatlineType(graphene.ObjectType):
    game_date = graphene.types.datetime.DateTime()
    mp = graphene.Float()
    fg = graphene.Float()
    fga = graphene.Float()
    fg_pct = graphene.Float()
    tp = graphene.Float()
    tpa = graphene.Float()
    tp_pct = graphene.Float()
    ft = graphene.Float()
    fta = graphene.Float()
    ft_pct = graphene.Float()
    orb = graphene.Float()
    drb = graphene.Float()
    trb = graphene.Float() 
    ast = graphene.Float()
    stl = graphene.Float()
    blk = graphene.Float()
    tov = graphene.Float()
    pf = graphene.Float()
    pts = graphene.Float()
    plus_minus = graphene.Float()
    gp = graphene.Float()
    starts = graphene.Float()
    started = graphene.Boolean()
    ts = graphene.Float()
    efg = graphene.Float()
    tpar = graphene.Float()
    ftr = graphene.Float()
    orb_pct = graphene.Float()
    drb_pct = graphene.Float()
    trb_pct = graphene.Float()
    ast_pct = graphene.Float()
    stl_pct = graphene.Float()
    blk_pct = graphene.Float()
    tov_pct = graphene.Float()
    usg_rate = graphene.Float()
    ortg = graphene.Float()
    drtg = graphene.Float()
    possessions = graphene.Float()
    pace = graphene.Float()

class FullStatlineListType(graphene.ObjectType):
    mp = graphene.List(graphene.Float)
    fg = graphene.List(graphene.Float)
    fga = graphene.List(graphene.Float)
    fg_pct = graphene.List(graphene.Float)
    tp = graphene.List(graphene.Float)
    tpa = graphene.List(graphene.Float)
    tp_pct = graphene.List(graphene.Float)
    ft = graphene.List(graphene.Float)
    fta = graphene.List(graphene.Float)
    ft_pct = graphene.List(graphene.Float)
    orb = graphene.List(graphene.Float)
    drb = graphene.List(graphene.Float)
    trb = graphene.List(graphene.Float)
    ast = graphene.List(graphene.Float)
    stl = graphene.List(graphene.Float)
    blk = graphene.List(graphene.Float)
    tov = graphene.List(graphene.Float)
    pf = graphene.List(graphene.Float)
    pts = graphene.List(graphene.Float)
    plus_minus = graphene.List(graphene.Float)
    gp = graphene.List(graphene.Float)
    starts = graphene.List(graphene.Float)
    started = graphene.List(graphene.Boolean)
    ts = graphene.List(graphene.Float)
    efg = graphene.List(graphene.Float)
    tpar = graphene.List(graphene.Float)
    ftr = graphene.List(graphene.Float)
    orb_pct = graphene.List(graphene.Float)
    drb_pct = graphene.List(graphene.Float)
    trb_pct = graphene.List(graphene.Float)
    ast_pct = graphene.List(graphene.Float)
    stl_pct = graphene.List(graphene.Float)
    blk_pct = graphene.List(graphene.Float)
    tov_pct = graphene.List(graphene.Float)
    usg_rate = graphene.List(graphene.Float)
    ortg = graphene.List(graphene.Float)
    drtg = graphene.List(graphene.Float)
    possessions = graphene.List(graphene.Float)
    pace = graphene.List(graphene.Float)
    game_dates = graphene.List(graphene.types.datetime.DateTime)


class AggregateStatlineType(graphene.ObjectType):
    averages = graphene.Field(FullStatlineType)
    standard_deviations = graphene.Field(FullStatlineType)



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
    aggregate_stats = graphene.Field(AggregateStatlineType)
    class Meta:
        model = Season

    def resolve_aggregate_stats(self, info):
        aggregate_stats = self.get_aggregate_stats()
        averages = aggregate_stats["averages"]
        standard_deviations = aggregate_stats["standard_deviations"]
        return AggregateStatlineType(
            averages=FullStatlineType(**averages), 
            standard_deviations=FullStatlineType(**standard_deviations))


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
    current_team = graphene.Field(TeamType)

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

    def resolve_current_team(self, info):
        latest_team_membership = PlayerTeamSeason.objects.filter(
            player=self, team_season__season__year=2019
        )
        return latest_team_membership.last().team_season.team


class PositionType(DjangoObjectType):
    class Meta:
        model = Position


class PlayerPositionType(DjangoObjectType):
    class Meta:
        model = PlayerPosition



class PlayerTeamSeasonType(DjangoObjectType):
    total_stats = graphene.Field(FullStatlineType)
    raw_stats = graphene.Field(FullStatlineListType)

    class Meta:
        model = PlayerTeamSeason

    def resolve_total_stats(self, info):
        total_stats = self.get_season_totals()
        return FullStatlineType(**total_stats)

    def resolve_raw_stats(self, info):
        raw_stats = self.get_raw_stats()
        return FullStatlineListType(**raw_stats)

class TeamSeasonType(DjangoObjectType):
    roster = graphene.List(PlayerTeamSeasonType)
    total_stats = graphene.Field(FullStatlineType)
    raw_stats = graphene.Field(FullStatlineListType)

    class Meta:
        model = TeamSeason

    def resolve_roster(self, info):
        return PlayerTeamSeason.objects.filter(team_season=self)

    def resolve_total_stats(self, info):
        total_stats = self.get_season_totals()
        return FullStatlineType(**total_stats)

    def resolve_raw_stats(self, info):
        raw_stats = self.get_raw_stats()
        return FullStatlineListType(**raw_stats)


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
    search = graphene.List(PlayerType, term=graphene.String())

    league = graphene.Field(
        LeagueType, id=graphene.Int(),name=graphene.String())
    conference = graphene.Field(
        ConferenceType, id=graphene.Int(), name=graphene.String())
    division = graphene.Field(
        DivisionType, id=graphene.Int(), name=graphene.String())
    location = graphene.Field(LocationType, id=graphene.Int())
    arena = graphene.Field(
        ArenaType, id=graphene.Int(), name=graphene.String())
    team = graphene.Field(
        TeamType, id=graphene.Int(), name=graphene.String(), 
        city=graphene.String(), abbr=graphene.String())
    person = graphene.Field(
        PersonType, id=graphene.Int(), name=graphene.String())
    player = graphene.Field(
        PlayerType, id=graphene.Int(), name=graphene.String())
    season = graphene.Field(
        SeasonType, year=graphene.Int(), league_id=graphene.Int())
    team_season = graphene.Field(
        TeamSeasonType, team_id=graphene.Int(), year=graphene.Int())
    player_team_season = graphene.Field(
        PlayerTeamSeasonType, player_id=graphene.Int(), 
        team_season_id=graphene.Int(), team_id=graphene.Int(), 
        year=graphene.Int())
    statlines = graphene.List(
        StatlineType, game_id=graphene.String())
    player_statlines = graphene.List(
        PlayerStatlineType, game_id=graphene.String(), 
        player_id=graphene.String())
    advanced_statlines = graphene.List(
        AdvancedStatlineType, statline_id=graphene.String())
    roster = graphene.List(PlayerTeamSeasonType)
    player_season = graphene.List(
        PlayerTeamSeasonType, player_id=graphene.Int(), year=graphene.Int())

    def resolve_search(self, info, **kwargs):
        term = kwargs.get("term")
        return Player.objects.filter(playerteamseason__isnull=False).annotate(
                similarity=Greatest(
                TrigramSimilarity('id__first_name', term), 
                TrigramSimilarity('id__last_name', term), 
                TrigramSimilarity('id__preferred_name', term)
            )).filter(similarity__gte=0.4).order_by('-similarity').distinct()

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
        return PlayerTeamSeason.objects.filter(player_id=player_id, team_season__season__year=year)

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

    def resolve_season(self, info, **kwargs):
        id = kwargs.get("league_id")
        year = kwargs.get("year")
        
        if id is not None:
            return Season.objects.get(pk=id)

        if year is not None and year > 1976:
            return Season.objects.get(year=year)

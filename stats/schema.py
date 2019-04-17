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

class PlayerType(DjangoObjectType):
    class Meta:
        model = Player


class PositionType(DjangoObjectType):
    class Meta:
        model = Position

class PlayerPositionType(DjangoObjectType):
    class Meta:
        model = PlayerPosition



class PlayerTeamSeasonType(DjangoObjectType):
    class Meta:
        model = PlayerTeamSeason

class TeamSeasonType(DjangoObjectType):
    roster = graphene.List(PlayerTeamSeasonType)
    class Meta:
        model = TeamSeason

    def resolve_roster(self, info):
        return PlayerTeamSeason.objects.filter(team_season=self)

class GameType(DjangoObjectType):
    class Meta:
        model = Game

class GamePeriodType(DjangoObjectType):
    class Meta:
        model = GamePeriod


class StatlineType(DjangoObjectType):
    class Meta:
        model = Statline

class AdvancedStatlineType(DjangoObjectType):
    class Meta:
        model = AdvancedStatline


class PlayerStatlineType(DjangoObjectType):
    class Meta:
        model = PlayerStatline

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

    league = graphene.Field(LeagueType, id=graphene.Int(), name=graphene.String())
    conference = graphene.Field(ConferenceType, id=graphene.Int(), name=graphene.String())
    division = graphene.Field(DivisionType, id=graphene.Int(), name=graphene.String())
    location = graphene.Field(LocationType, id=graphene.Int())
    arena = graphene.Field(ArenaType, id=graphene.Int(), name=graphene.String())
    team = graphene.Field(TeamType, id=graphene.Int(), name=graphene.String(), city=graphene.String(), abbr=graphene.String())
    person = graphene.Field(PersonType, name=graphene.String(), id=graphene.Int())
    player = graphene.Field(PlayerType, name=graphene.String(), id=graphene.Int())
    season = graphene.Field(SeasonType, year=graphene.Int())
    team_season = graphene.Field(TeamSeasonType, team_id=graphene.Int(), year=graphene.Int())
    player_team_season = graphene.Field(PlayerTeamSeasonType, player_id=graphene.Int(), team_season_id=graphene.Int())
    statlines = graphene.List(StatlineType, game_id=graphene.String())
    player_statlines = graphene.List(PlayerStatlineType, game_id=graphene.String(), player_id=graphene.String())
    advanced_statlines = graphene.List(AdvancedStatlineType, statline_id=graphene.String())
    roster = graphene.List(PlayerTeamSeasonType)
    
    def resolve_team_season(self, info, **kwargs):
        team_id = kwargs.get("team_id")
        year = kwargs.get("year")
        season = Season.objects.get(year=year, league_id=1)
        return TeamSeason.objects.get(team_id=team_id, season=season)

    # def resolve_roster(self, info, **kwargs):
    #     team_id = kwargs.get("team_id")
    #     year = kwargs.get("year")

    #     team = Team.objects.get(pk=team_id)
    #     players = team.get_roster(year)
    #     return players

    def resolve_all_teams(self, info, **kwargs):
        return Team.objects.all()
    
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
import graphene

from graphene_django.types import DjangoObjectType
from stats.models import League, Conference, Division, Location, Team, Arena, Logo

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

class LogoType(DjangoObjectType):
    class Meta:
        model = Logo


class Query(object):
    all_leagues = graphene.List(LeagueType)
    all_conferences = graphene.List(ConferenceType)
    all_divisions = graphene.List(DivisionType)
    all_locations = graphene.List(LocationType)
    all_arenas = graphene.List(ArenaType)
    all_teams = graphene.List(TeamType)
    all_logos = graphene.List(LogoType)

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
    
    def resolve_all_logos(self, info, **kwargs):
        return Logo.objects.all()
    
    league = graphene.Field(LeagueType, id=graphene.Int(), name=graphene.String())
    conference = graphene.Field(ConferenceType, id=graphene.Int(), name=graphene.String())
    division = graphene.Field(DivisionType, id=graphene.Int(), name=graphene.String())
    location = graphene.Field(LocationType, id=graphene.Int())
    arena = graphene.Field(ArenaType, id=graphene.Int(), name=graphene.String())
    team = graphene.Field(TeamType, id=graphene.Int(), name=graphene.String(), city=graphene.String(), abbr=graphene.String())
    logo = graphene.Field(TeamType, id=graphene.Int())

    def resolve_league(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return League.objects.get(pk=id)

        if name is not None:
            return League.objects.get(name=name)
    
    def resolve_conference(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Conference.objects.get(pk=id)

        if name is not None:
            return Conference.objects.get(name=name)
    

    def resolve_division(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Division.objects.get(pk=id)

        if name is not None:
            return Division.objects.get(name=name)
    
    def resolve_location(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Location.objects.get(pk=id)
    
    def resolve_arena(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Arena.objects.get(pk=id)
    
        if name is not None:
            return Arena.objects.get(name=name)
    

    def resolve_team(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')
        abbr = kwargs.get('abbr')

        if id is not None:
            return Team.objects.get(pk=id)

        if name is not None:
            return Team.objects.get(name=name)

        if abbr is not None:
            return Team.objects.get(abbreviation=abbr)
    
    def resolve_logo(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Logo.objects.get(pk=id)
    

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
    
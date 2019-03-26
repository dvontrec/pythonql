import graphene
# tells graphene django about the track model
from .models import Track
from graphene_django import DjangoObjectType


class TrackType(DjangoObjectType):
    class meta:
        model = Track


# root query
class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType)

    # tracks resolver
    def resolve_tracks(self, info):
        # returns all tracks
        return Track.objects.all()

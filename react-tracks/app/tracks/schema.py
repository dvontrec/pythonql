import graphene
from graphene_django import DjangoObjectType
# tells graphene django about the track model
from .models import Track


class TrackType(DjangoObjectType):
    class Meta:
        model = Track


# root query
class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType)

    # tracks resolver
    def resolve_tracks(self, info):
        # returns all tracks
        return Track.objects.all()

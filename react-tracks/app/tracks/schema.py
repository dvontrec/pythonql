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


# create tracks class
class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    # resolver
    def mutate(self, info, title, description, url):
        track = Track(title=title, description=description, url=url)
        # saves track to database
        track.save()
        return CreateTrack(track=track)


# base mutation class
class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()

import graphene
import tracks.schema


# root query
class Query(tracks.schema.Query, graphene.ObjectType):
    pass


# root Mutation
class Mutation(tracks.schema.Mutation, graphene.ObjectType):
    pass


# creates a schema
schema = graphene.Schema(query=Query, mutation=Mutation)

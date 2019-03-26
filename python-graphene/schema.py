import graphene
import json

# creates a root query type that subclasses from graphine.ObjectType


class Query (graphene.ObjectType):
    # specifies that the hello field is of type string
    hello = graphene.String()

    # resolver function that resolves the query operation
    def resolve_hello(self, info):
        return "world"


schema = graphene.Schema(query=Query)

result = schema.execute(
    '''
  {
    hello
  }
  '''
)

#  prints the query results as json
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2))

import graphene
import json
from datetime import datetime

# Creates a user data class


class User (graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    created_at = graphene.DateTime()


# creates a root query type that subclasses from graphine.ObjectType
class Query (graphene.ObjectType):
    # Users query will return a list of users
    users = graphene.List(User, limit=graphene.Int())
    # specifies that the hello query will return a string
    hello = graphene.String()
    # the is_admin query will return a boolean
    is_admin = graphene.Boolean()

    # resolver function that resolves the query operation
    def resolve_hello(self, info):
        return "world"

    # resolver function for if is admin
    def resolve_is_admin(self, info):
        return True

    # resolve function for getting users
    def resolve_users(self, info, limit=None):
        return [
            User(id="1", username="Q", created_at=datetime.now()),
            User(id="2", username="Smoke", created_at=datetime.now())
        ][:limit]  # Slices the list to only include the limit of users returned


schema = graphene.Schema(query=Query)

# queries from the user query with data needed specified
result = schema.execute(
    '''
  {
    users{
      id,
      username
      createdAt
    }
  }
  '''
)

#  prints the query results as json
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2))

import graphene
import json
import uuid
from datetime import datetime


# class representing user Post data
class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()


# Creates a user data class
class User (graphene.ObjectType):
    id = graphene.ID(default_value=uuid.uuid4())
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
    avatar_url = graphene.String()

    def resolve_avatar_url(self, info):
        # returns a url created using the username and the id
        return 'https://imageservice.com/{}/{}'.format(self.username, self.id)


# Creates a class for creating users
class CreateUser(graphene.Mutation):
    user = graphene.Field(User)
    # defined the arguments the mutation recieves

    class Arguments:
        # Username will be the only field we pass to the mutation
        username = graphene.String()

    # resolver functions are always called mutate
    def mutate(self, info, username):
        user = User(username=username)
        return CreateUser(user=user)


class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    # Mutate resolver
    def mutate(self, info, title, content):
        # grabs contect value and if the user is anonymous raise an exception
        if info.context.get('is_anonymous'):
            raise Exception('Not authenticated')
        post = Post(title=title, content=content)
        return CreatePost(post=post)


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
        # returns a list of users
        return [
            User(username="Q", created_at=datetime.now()),
            User(username="Smoke", created_at=datetime.now())
        ][:limit]  # Slices the list to only include the limit of users returned


# adds a Mutation class
class Mutation(graphene.ObjectType):
    # createUser mutation used to make new users
    create_user = CreateUser.Field()
    # cteatePost mutation used to create new user posts
    create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

# queries from the user query with data needed specified
result = schema.execute(
    '''
  {
    users{
      id,
      username
      createdAt
      avatarUrl
    }
  }
  '''
)

# queries a mutation to create a user
result1 = schema.execute(
    '''
  mutation($username: String!){
    createUser(username: $username){
      user{
        id
        username
        createdAt
      }
    }
  }
  ''',
    variable_values={'username': 'Dev'}
)

# queries with a limit provided as a variable
result2 = schema.execute(
    '''
    query getUsersQuery ($limit: Int!){
      users(limit: $limit){
        id
        username
        createdAt
      }
    }
  ''',
    variable_values={'limit': 1}
)

# queries a mutatin to create a new post
result3 = schema.execute(
    '''
  mutation {
    createPost(title: "hello", content:"world"){
      post{
        title
        content
      }
    }
  }
  ''', context={'is_anonymous': False}
)
#  prints the query results as json
dictResult = dict(result3.data.items())
print(json.dumps(dictResult, indent=2))

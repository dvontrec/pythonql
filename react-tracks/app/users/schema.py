from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType


# base user class
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


# create user class
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    # Arguments used to create new users
    class Arguments:
        # all arguments are required
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    # create user mutation function
    def mutate(self, info, username, password, email):
        # Used django usermodel to create a user
        user = get_user_model()(
            username=username,
            email=email
        )
        # sets the user password to the passed password
        user.set_password(password)
        # saves the user
        user.save()


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

import graphene

from tahaApp.schema import TahaQuery, TahaMutation
import graphql_jwt


class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(
    TahaQuery,  # Add your Query objects here
    graphene.ObjectType
):
    pass


class Mutation(AuthMutation, TahaMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

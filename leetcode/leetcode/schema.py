import graphene
import graphql_jwt

import problems.schema
import users.schema
import problems.schema_relay




class Query(problems.schema.Query, users.schema.Query, problems.schema_relay.RelayQuery,graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation,problems.schema.Mutation, problems.schema_relay.RelayMutation,graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    pass


schema = graphene.Schema(query=Query, mutation = Mutation)
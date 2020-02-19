import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Problem, Mock

#1
class ProblemFilter(django_filters.FilterSet):
    class Meta:
        model = Problem
        fields = ['url', 'company']


#2
class ProblemNode(DjangoObjectType):
    class Meta:
        model = Problem
        #3
        interfaces = (graphene.relay.Node, )


class MockNode(DjangoObjectType):
    class Meta:
        model = Mock
        interfaces = (graphene.relay.Node,)


class RelayQuery(graphene.ObjectType):
    #4
    relay_problem = graphene.relay.Node.Field(ProblemNode)
    #5
    relay_problems = DjangoFilterConnectionField(ProblemNode, filterset_class=ProblemFilter)


class RelayCreateProblem(graphene.relay.ClientIDMutation):
    problem = graphene.Field(ProblemNode)

    class Input:
        url = graphene.String()
        company = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user or None

        problem = Problem(
            url=input.get('url'),
            companyn=input.get('company'),
            posted_by=user,
        )
        problem.save()

        return RelayCreateProblem(problem = problem)


class RelayMutation(graphene.AbstractType):
    relay_create_problem = RelayCreateProblem.Field()
import graphene
from graphene_django import DjangoObjectType
from .models import Problem
from users.schema import UserType
from problems.models import Problem, Mock
from graphql import GraphQLError
from django.db.models import Q


class ProblemType(DjangoObjectType):
    class Meta:
        model = Problem 

class MockType(DjangoObjectType):
    class Meta:
        model = Mock

class Query(graphene.ObjectType):
    problems = graphene.List(ProblemType, search=graphene.String(), first = graphene.Int(), skip =graphene.Int(),)
    mocks = graphene.List(MockType)

    def resolve_problems(self, info,search=None, **kwargs):
        qs = Problem.objects.all()
        if search:
            filter = (
                Q(url__icontains=search) |
                Q(company__icontains=search)
            )
            qs = qs.filter(filter)
        
        if skip:
            qs = qs[skip:]
            
        if first:
            qs = qs[first:]

        return qs

    def resolve_mocks(self, info, **kwargs):
        return Mock.objects.all()


class CreateMock(graphene.Mutation):
    user = graphene.Field(UserType)
    problem = graphene.Field(MockType)

    class Arguments:
        problem_id = graphene.Int()

    def mutate(self, info, problem_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You must be logged to interview!')

        problem = Problem.objects.filter(id=problem_id).first()
        if not problem:
            raise Exception('Invalid Link!')

        Mock.objects.create(
            user=user,
            problem=problem,
        )

        return CreateMock(user=user, problem=problem)

class CreateProblem(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    company = graphene.String()
    posted_by = graphene.Field(UserType)

    #2
    class Arguments:
        url = graphene.String()
        company = graphene.String()
    #3
    def mutate(self, info, url, company):
        user = info.context.user or None

        problem = Problem(
            url=url,
            company=company,
            posted_by=user,
        )
        problem.save()

        return CreateProblem(
            id = problem.id,
            url = problem.url,
            company = problem.company,
            posted_by = problem.post_by,
        )


#4
class Mutation(graphene.ObjectType):
    create_problem = CreateProblem.Field()
    create_mock = CreateMock.Field()


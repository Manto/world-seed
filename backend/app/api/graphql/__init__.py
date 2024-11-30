import strawberry
from .queries import Query
from .mutations import Mutation

# Create and export the GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

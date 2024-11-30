from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.graphql import schema
from app.api.graphql.context import get_context
from strawberry.fastapi import GraphQLRouter
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database with default data
    init_db()
    yield


app = FastAPI(title="Worldbuilding API", lifespan=lifespan)
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQL route with context
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

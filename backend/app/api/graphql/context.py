from typing import AsyncGenerator
from strawberry.fastapi import BaseContext
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database import get_async_session


class GraphQLContext(BaseContext):
    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db


async def get_context(
    db: AsyncSession = Depends(get_async_session),
) -> GraphQLContext:
    return GraphQLContext(db=db)

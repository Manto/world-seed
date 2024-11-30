from typing import Any, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import BaseContext
from app.database import get_db
from app.ai.service import AIService
from app.config import settings


class GraphQLContext(BaseContext):
    def __init__(self, db: AsyncSession, ai_service: AIService):
        super().__init__()
        self.db = db
        self.ai_service = ai_service


async def get_context(
    db: AsyncSession = get_db(),
) -> AsyncGenerator[GraphQLContext, Any]:
    ai_service = AIService(settings.ANTHROPIC_API_KEY)
    yield GraphQLContext(db=db, ai_service=ai_service)

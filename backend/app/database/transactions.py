from typing import TypeVar, Callable, Awaitable, Any
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

T = TypeVar("T")


class TransactionError(Exception):
    """Custom exception for transaction-related errors"""

    pass


def handle_transaction_error(error: Exception) -> None:
    """Convert database errors to appropriate HTTP responses"""
    if isinstance(error, SQLAlchemyError):
        raise HTTPException(
            status_code=500, detail="Database error occurred"
        ) from error
    elif isinstance(error, TransactionError):
        raise HTTPException(status_code=400, detail=str(error))
    raise error


def transactional(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    """
    Decorator to handle database transactions.
    Ensures that database operations are atomic and properly rolled back on error.
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        # Find the session in the arguments
        session = None
        for arg in args:
            if isinstance(arg, AsyncSession):
                session = arg
                break
        if session is None:
            for arg in kwargs.values():
                if isinstance(arg, AsyncSession):
                    session = arg
                    break

        if session is None:
            raise ValueError("No database session found in arguments")

        try:
            result = await func(*args, **kwargs)
            await session.commit()
            return result
        except Exception as e:
            await session.rollback()
            handle_transaction_error(e)

    return wrapper

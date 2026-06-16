"""Database engine, session factory, and base model configuration for the application."""

import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # disable in production
    pool_size=10,  # number of connections kept open
    max_overflow=20,  # extra connections allowed under peak load
    pool_recycle=3600,  # recycle connections after 1 hour to prevent MySQL dropping them silently
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


async def get_db():
    """Yields an async database session for use as a FastAPI dependency.

    Yields:
        AsyncSession: An active SQLAlchemy async session.
    """
    async with AsyncSessionLocal() as session:
        yield session

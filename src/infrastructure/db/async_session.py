"""Асинхронное подключение к БД (для FastAPI + asyncpg)."""

from __future__ import annotations

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import get_settings

_settings = get_settings()
async_engine = create_async_engine(_settings.async_database_url, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, autoflush=False, expire_on_commit=False)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    """Зависимость FastAPI: выдаёт async-сессию на время запроса."""
    async with AsyncSessionLocal() as session:
        yield session

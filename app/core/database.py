from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine=create_async_engine(settings.DATABASE_URL_asyncpg, echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
class Base(DeclarativeBase):
    pass
async def get_async_session()->AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
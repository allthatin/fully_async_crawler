from redis import asyncio as pyaioredis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

from config import DATABASE_URI, REDIS_HOST, REDIS_PORT
from database.models import Base


async def get_redis_connection():
    return await pyaioredis.create_redis_pool(
        (REDIS_HOST, REDIS_PORT), db=0  # Replace db with appropriate database number if needed
    )

async def get_async_engine():
    engine = create_async_engine(DATABASE_URI)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Create tables if not exist
    return engine


@asynccontextmanager
async def get_async_session():
    engine = await get_async_engine()
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        yield session

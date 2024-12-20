from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from app.database.config import db_setting


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


async_engine = create_async_engine(db_setting.database_url, echo=True)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    try:
        async with async_session_maker() as session:
            yield session
    except SQLAlchemyError as e:
        pass

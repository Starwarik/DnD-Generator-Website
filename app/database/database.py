from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase
from .config import db_setting

engine = create_engine(db_setting.database_url, echo=True)


def create_db_and_tables():
    Base.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


class Base(DeclarativeBase):
    __abstract__ = True
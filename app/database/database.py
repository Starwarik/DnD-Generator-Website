from sqlmodel import create_engine, SQLModel, Session
from .config import db_setting

engine = create_engine(db_setting.database_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

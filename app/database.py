from sqlmodel import create_engine, SQLModel
from app.config import settings

engine = create_engine(settings.database_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

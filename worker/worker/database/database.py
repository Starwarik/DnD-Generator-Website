from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    sync_database_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


db_setting = DBSettings()


class Base(DeclarativeBase):
    __abstract__ = True


engine = create_engine(db_setting.sync_database_url)
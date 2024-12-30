from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    sync_database_url: str = Field(..., env='SYNC_DATABASE_URL')

    model_config = SettingsConfigDict(secrets_dir="/run/secrets", extra="ignore")


db_setting = DBSettings()


class Base(DeclarativeBase):
    __abstract__ = True


engine = create_engine(db_setting.sync_database_url, echo=True)


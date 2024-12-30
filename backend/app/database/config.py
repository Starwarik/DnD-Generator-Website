from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    database_url: str = Field(..., env='DATABASE_URL')

    model_config = SettingsConfigDict(secrets_dir="/run/secrets", extra="ignore")


db_setting = DBSettings()

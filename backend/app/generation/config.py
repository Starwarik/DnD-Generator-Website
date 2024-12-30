from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GenerationSettings(BaseSettings):
    min_balance_to_generate: float

    model_config = SettingsConfigDict(extra="ignore")


generation_setting = GenerationSettings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class GenerationSettings(BaseSettings):
    gigachat_credentials: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


generation_setting = GenerationSettings()

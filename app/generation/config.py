from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class GenerationSettings(BaseSettings):
    gigachat_credentials: str
    yandexchat_api_key: SecretStr
    yandexchat_folder_id: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


generation_setting = GenerationSettings()

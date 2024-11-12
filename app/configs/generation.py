from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class GenerationSettings(BaseSettings):
    gigachat_credentials: str
    yandexchat_api_key: SecretStr
    yandexchat_folder_id: str

    min_balance_to_generate: float

    gigachat_prompt_token_cost: float
    gigachat_assistant_token_cost: float
    yandexgpt_prompt_token_cost: float
    yandexgpt_assistant_token_cost: float
    image_generated_cost: float

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


generation_setting = GenerationSettings()

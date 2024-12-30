from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GenerationSettings(BaseSettings):
    gigachat_credentials: str = Field(..., env='GIGACHAT_CREDENTIALS')
    yandexchat_api_key: SecretStr = Field(..., env='YANDEXCHAT_API_KEY')
    yandexchat_folder_id: str = Field(..., env='YANDEXCHAT_FOLDER_ID')

    min_balance_to_generate: float

    gigachat_prompt_token_cost: float
    gigachat_assistant_token_cost: float
    yandexgpt_prompt_token_cost: float
    yandexgpt_assistant_token_cost: float 
    image_generated_cost: float

    model_config = SettingsConfigDict(secrets_dir="/run/secrets", extra="ignore")


generation_setting = GenerationSettings()

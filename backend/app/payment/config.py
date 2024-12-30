from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class PaymentSettings(BaseSettings):
    secret_key_jwt: str = Field(..., env='SECRET_KEY_JWT')
    algorithm_jwt: str
    token_expire_minutes: int

    model_config = SettingsConfigDict(secrets_dir="/run/secrets", extra="ignore")


payment_setting = PaymentSettings()


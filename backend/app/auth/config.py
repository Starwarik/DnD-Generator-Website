from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class AuthSettings(BaseSettings):
    secret_key_jwt: str = Field(..., env='SECRET_KEY_JWT')
    algorithm_jwt: str = Field(..., env='ALGORITHM_JWT')
    token_expire_minutes: int = Field(..., env='TOKEN_EXPIRE_MINUTES')

    model_config = SettingsConfigDict(secrets_dir="/run/secrets", extra="ignore")


auth_setting = AuthSettings()

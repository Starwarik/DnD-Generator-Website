from pydantic_settings import BaseSettings, SettingsConfigDict

class AuthSettings(BaseSettings):
    secret_key_jwt: str
    algorithm_jwt: str

    token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

auth_setting = AuthSettings()
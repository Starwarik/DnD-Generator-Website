from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    is_test: bool
    docs_url: str
    openapi_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


app_setting = AppSettings()

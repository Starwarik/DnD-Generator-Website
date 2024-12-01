from pydantic_settings import BaseSettings, SettingsConfigDict


class ImageSettings(BaseSettings):
    test_image_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


image_setting = ImageSettings()

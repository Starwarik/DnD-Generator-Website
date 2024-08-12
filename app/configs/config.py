from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum


class NotificationServiceChoice(Enum):
    dummy_notification = "dummy_notification"
    smtp_notification = "smtp_notification"


class Settings(BaseSettings):
    notification_service: NotificationServiceChoice

    secret_key_jwt: str
    algorithm_jwt: str

    token_expire_minutes: int

    database_url: str

    model_config = SettingsConfigDict(env_file="configs/.env")


class SMTPData(BaseSettings):
    server_url: str
    server_port: int
    sender_email: str
    login: str
    password: str
    template_subject: str
    template_message: str

    model_config = SettingsConfigDict(env_file="configs/.envsmtp")


settings = Settings()
smtp_settings = SMTPData()

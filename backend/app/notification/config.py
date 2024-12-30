from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum
from pydantic import Field


class NotificationServiceChoice(Enum):
    dummy_notification = "dummy_notification"
    smtp_notification = "smtp_notification"


class NotificationSettings(BaseSettings):
    notification_service: NotificationServiceChoice 

    smtp_server_url: str 
    smtp_server_port: int 
    smtp_sender_email: str 
    smtp_login: str
    smtp_password: str = Field(..., env='SMTP_PASSWORD')
    smtp_template_subject: str 
    smtp_template_message: str 

    model_config = SettingsConfigDict(secrets_dir="/run/secrets", extra="ignore")


notification_setting = NotificationSettings()

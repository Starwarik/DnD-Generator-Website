from pydantic_settings import BaseSettings, SettingsConfigDict


class PaymentSettings(BaseSettings):
    vtb_username: str
    vtb_password: str

    vtb_base_api: str

    url_successful_order: str
    url_failed_order: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


payment_setting = PaymentSettings()

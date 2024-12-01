from app.notification.notifications import notification_service
from app.database.database import create_db_and_tables

from contextlib import asynccontextmanager
from fastapi import FastAPI

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    is_test: bool
    docs_url: str
    openapi_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


app_setting = AppSettings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global notification_service
    await create_db_and_tables()
    notification_service.start()
    yield
    notification_service.stop()


def create_application(is_test: bool):
    return FastAPI(
        lifespan=lifespan,
        openapi_url=app_setting.openapi_url if is_test else None,
        docs_url=app_setting.docs_url if is_test else None
        debug=is_test,
        redoc_url=None,
    )

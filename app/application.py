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


if app_setting.is_test:
    app = FastAPI(
        lifespan=lifespan,
        openapi_url=app_setting.openapi_url,
        docs_url=app_setting.docs_url,
        redoc_url=None,
    )
else:
    app = FastAPI(lifespan=lifespan, openapi_url=None, docs_url=None, redoc_url=None)

from app.notification.notifications import notification_service
from app.database.database import create_db_and_tables


from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.app.config import app_setting


@asynccontextmanager
async def lifespan(app: FastAPI):
    global notification_service
    create_db_and_tables()
    notification_service.start()
    yield
    notification_service.stop()


if app_setting.is_adding_docs:
    app = FastAPI(
        lifespan=lifespan,
        openapi_url=app_setting.openapi_url,
        docs_url=app_setting.docs_url,
        redoc_url=None,
    )
else:
    app = FastAPI(lifespan=lifespan, openapi_url=None, docs_url=None, redoc_url=None)

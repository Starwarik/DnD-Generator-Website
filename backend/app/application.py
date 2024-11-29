from app.notification.notifications import notification_service
from app.database.database import create_db_and_tables


from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.configs.app import app_setting


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
        debug=True,
        redoc_url=None,
    )
else:
    app = FastAPI(lifespan=lifespan, openapi_url=None, docs_url=None, redoc_url=None)

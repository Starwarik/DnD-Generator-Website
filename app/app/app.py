from app.notification.notifications import notification_service
from app.database.database import create_db_and_tables


from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    global notification_service
    create_db_and_tables()
    notification_service.start()
    yield
    notification_service.stop()


app = FastAPI(lifespan=lifespan)

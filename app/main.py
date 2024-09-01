from contextlib import asynccontextmanager


from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from app.notification.notifications import notification_service
from app.database.database import create_db_and_tables
from app.database.crud import *
from app.auth.router import auth_router
from app.user.router import user_router
from app.generation.router import generation_router
from app.image.router import image_router
from app.adventure.router import adventure_router


class TokenData(BaseModel):
    username: Union[str, None] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global notification_service
    create_db_and_tables()
    notification_service.start()
    yield
    notification_service.stop()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(generation_router)
app.include_router(adventure_router)
app.include_router(image_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

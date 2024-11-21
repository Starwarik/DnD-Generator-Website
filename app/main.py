from typing import Union

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from app.application import *
from app.database.crud import *
from app.auth.router import auth_router
from app.user.router import user_router
from app.generation.router import generation_router
from app.image.router import image_router
from app.adventure.router import adventure_router
from app.test_function.router import test_router


class TokenData(BaseModel):
    username: Union[str, None] = None


app = create_application(app_setting.is_test)

routers = [auth_router, user_router, generation_router, adventure_router, image_router]
for router in routers:
    app.include_router(router)

if app_setting.is_test:
    app.include_router(test_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

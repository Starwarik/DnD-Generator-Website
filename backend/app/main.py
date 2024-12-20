from typing import Union

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from app.application import *
from app.database.crud import *
from app.test_function.router import test_router
from app.auth.router import auth_router
from app.user.router import user_router
from app.payment.router import payment_router
from app.adventure.router import adventure_router
from app.generation.router import generation_router
from app.image.router import image_router


class TokenData(BaseModel):
    username: Union[str, None] = None


app = create_application(app_setting.is_test)

if app_setting.is_test:
    app.include_router(test_router)

routers = [auth_router, user_router, payment_router, adventure_router, generation_router, image_router]
for router in routers:
    app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

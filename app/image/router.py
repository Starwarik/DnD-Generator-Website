from sqlalchemy.orm import Session
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, Response

from app.auth.dependencies import get_current_user
from app.database.database import get_session
from app.image.service import get_image_by_id
from app.user.models import User
from fastapi.responses import FileResponse
from app.configs.image import image_setting

image_router = APIRouter(tags=["image"])


@image_router.get("/api/images/{image_id}")
def get_image(
    image_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    if image_id == -42:
        return FileResponse(image_setting.test_image_url)
    try:
        image = get_image_by_id(image_id, current_user.id, session)
        if image is None:
            return None
        return Response(content=image.image, media_type=image.media_type)
    except Exception:
        return Response(status_code=404)

import os
from celery import Celery
from kombu.serialization import register
from schemas import AdventureUpdateWithSpentedResult, AdventureInfo
from generation_text_service import (
    generate_new_adventure_json,
    generate_new_test_adventure_json,
)
from text_models import text_generation_model

import pydanticserializer

CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

register(
    "pydantic",
    pydanticserializer.pydantic_dumps,
    pydanticserializer.pydantic_loads,
    content_type="application/x-pydantic",
    content_encoding="utf-8",
)

celery_app = Celery("celery", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    task_serializer="pydantic",
    result_serializer="pydantic",
    event_serializer="pydantic",
    accept_content=["application/json", "application/x-pydantic"],
    result_accept_content=["application/json", "application/x-pydantic"],
)


@celery_app.task(name="main.generate_new_adventure")
def generate_new_adventure(
    location_name: str, setting: str, num_players: int
) -> AdventureUpdateWithSpentedResult:
    return generate_new_adventure_json(
        location_name, setting, num_players, text_generation_model
    )


@celery_app.task(name="main.generate_new_test_adventure")
def generate_new_test_adventure(
    location_name: str, setting: str, num_players: int
) -> AdventureUpdateWithSpentedResult:
    return generate_new_test_adventure_json(location_name, setting, num_players)

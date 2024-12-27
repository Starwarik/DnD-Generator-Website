import os
from celery import Celery
from kombu.serialization import register

import worker.pydanticserializer as pydanticserializer

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

celery_app.autodiscover_tasks(
    ["worker.text_tasks", "worker.image_tasks", "worker.payment"]
)

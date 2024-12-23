import os
from celery import Celery
from celery import signature, chain


CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

celery_app = Celery("celery", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

task = chain(
    signature("main.test_task", args=(1, 2)),
    signature("main.test_task", args=(3,)),
    signature("main.test_task", args=(4,)),
)()
print(task.get())

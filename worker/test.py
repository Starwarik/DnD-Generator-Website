import os
from celery import Celery


CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

celery_app = Celery("celery", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

task = celery_app.send_task(
    "main.generate_new_test_adventure", args=["Храм Грача", "Фентези", 2]
)
print(task.id)
print(task.get())

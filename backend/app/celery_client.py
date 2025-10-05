from celery import Celery
from datetime import datetime
from app.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)


def schedule_task_completion(task_id: int, due_date: datetime):
    result = celery_app.send_task(
        "app.celery_worker.complete_task",
        args=[task_id],
        eta=due_date
    )

    return result


def revoke_task(task_id: str):
    celery_app.control.revoke(task_id, terminate=True)

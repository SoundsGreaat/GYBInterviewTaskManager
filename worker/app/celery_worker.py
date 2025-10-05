from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import logging

from app.config import settings
from app.models import Task, TaskStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
)

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@celery_app.task(name="app.celery_worker.complete_task", bind=True)
def complete_task(self, task_id: int):
    logger.info(f"Completing task {task_id}")

    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            logger.warning(f"Task {task_id} not found")
            return {"status": "error", "message": "Task not found"}

        if task.status == TaskStatus.done:
            logger.info(f"Task {task_id} already completed")
            return {"status": "skipped", "message": "Task already completed"}

        # TODO: Add task processing logic here (e.g., data processing, external API calls)

        task.status = TaskStatus.done
        task.updated_at = datetime.datetime.now(datetime.UTC)
        db.commit()

        logger.info(f"Task {task_id} completed successfully")
        return {
            "status": "success",
            "task_id": task_id,
            "completed_at": datetime.datetime.now(datetime.UTC).isoformat()
        }

    except Exception as e:
        logger.error(f"Error completing task {task_id}: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

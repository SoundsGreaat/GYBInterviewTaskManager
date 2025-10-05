import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app import schemas, models
from app.celery_client import schedule_task_completion, revoke_task
from app.llm_client import generate_short_description


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    db_task = models.Task(
        title=task.title,
        description=task.description,
        short_description=generate_short_description(
            task.title,
            task.description,
            task.text
        ),
        text=task.text,
        due_date=task.due_date,
        status=models.TaskStatus.pending
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    celery_task = schedule_task_completion(db_task.id, task.due_date)
    db_task.celery_task_id = celery_task.id
    db.commit()
    db.refresh(db_task)

    return db_task


def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
) -> List[models.Task]:
    query = db.query(models.Task)

    if status:
        query = query.filter(models.Task.status == status)

    return query.order_by(models.Task.due_date).offset(skip).limit(limit).all()


def update_task(
        db: Session,
        task_id: int,
        task: schemas.TaskUpdate
) -> Optional[models.Task]:
    db_task = get_task(db, task_id)
    if not db_task:
        return None

    update_data = task.model_dump(exclude_unset=True)

    if "due_date" in update_data and db_task.status == models.TaskStatus.pending:
        if db_task.celery_task_id:
            revoke_task(db_task.celery_task_id)

        celery_task = schedule_task_completion(task_id, update_data["due_date"])
        update_data["celery_task_id"] = celery_task.id

    if "status" in update_data and update_data["status"] == models.TaskStatus.done:
        if db_task.celery_task_id:
            revoke_task(db_task.celery_task_id)

    for key, value in update_data.items():
        setattr(db_task, key, value)

    db_task.updated_at = datetime.datetime.now(datetime.UTC)
    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    db_task = get_task(db, task_id)
    if not db_task:
        return False

    if db_task.celery_task_id:
        revoke_task(db_task.celery_task_id)

    db.delete(db_task)
    db.commit()
    return True

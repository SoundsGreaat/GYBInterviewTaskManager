import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import engine, get_db
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="API for managing tasks with automatic status updates using Celery.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "message": "Task Manager API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post("/tasks/", response_model=schemas.Task, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.

    Automatically schedules a Celery task to mark it as 'done' at due_date.
    """
    return crud.create_task(db=db, task=task)


@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(
        skip: int = 0,
        limit: int = 100,
        status: str = None,
        db: Session = Depends(get_db)
):
    """
    Get a list of tasks with optional status filtering.
    """
    tasks = crud.get_tasks(db, skip=skip, limit=limit, status=status)
    return tasks


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    Get a task by ID.
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(
        task_id: int,
        task: schemas.TaskUpdate,
        db: Session = Depends(get_db)
):
    """
    Update a task.
    
    If due_date is changed, reschedules the corresponding Celery task.
    If status is manually set to 'done', cancels the Celery task.
    """
    db_task = crud.update_task(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by ID.

    Cancels the scheduled Celery task if it exists.
    """
    success = crud.delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }

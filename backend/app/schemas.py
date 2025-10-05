from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models import TaskStatus


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: str = Field(..., min_length=1, description="Task description")
    text: str = Field(..., min_length=1, description="Task detailed text")
    due_date: datetime = Field(..., description="Task due date and time")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    text: Optional[str] = Field(None, min_length=1)
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None


class Task(TaskBase):
    id: int
    status: TaskStatus
    celery_task_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

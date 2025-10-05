from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
import datetime
import enum

Base = declarative_base()


class TaskStatus(str, enum.Enum):
    pending = "pending"
    done = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    short_description = Column(String(128), nullable=True)
    text = Column(Text, nullable=False)
    due_date = Column(DateTime, nullable=False, index=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending, nullable=False, index=True)
    celery_task_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC),
                        onupdate=datetime.datetime.now(datetime.UTC), nullable=False)
    
# Project Structure

backend/ — Main API application (FastAPI/Flask), database models, migrations, and business logic.

worker/ — Celery worker for processing background tasks.

docker-compose.yml — Multi-container orchestration for backend, worker, database, and message broker.

README.MD — Project documentation.

# Development

## Requirements

- Docker and Docker Compose.

## Running Locally

1. Clone the repository.
2. Navigate to the project directory.
3. Run `docker-compose up --build` to start all services.
4. Access the API at `http://localhost:8000`.

### Note on Environment Variables

- All environment variables are defined directly in `docker-compose.yml`.
- For production, consider using a `.env` file or a secrets manager to handle sensitive information.
- If you want to override variables, edit them directly in `docker-compose.yml`.
- The only required environment variable is `GEMINI_API_KEY` for the language model API. Please set it in
  `docker-compose.yml` before running the services.

# API Documentation

- The API documentation is available at `http://localhost:8000/docs` (Swagger UI) when the backend service is running.

## Endpoints

- ### `POST /tasks/` - Create a new task.

```json
POST /tasks/
Content-Type: application/json

{
"title": "Complete the project",
"description": "Finish implementing the Task Manager",
"text": "Add all features and test the system",
"due_date": "2025-00-00T00:00:00"
}
```

Response:

```json
{
  "id": 1,
  "title": "Complete the project",
  "description": "Finish implementing the Task Manager",
  "text": "Add all features and test the system",
  "due_date": "2025-00-00T00:00:00",
  "status": "pending",
  "celery_task_id": "abc123-def456-...",
  "created_at": "2025-00-00T00:00:00",
  "updated_at": "2025-00-00T00:00:00"
}
```

- ### `GET /tasks/` - Retrieve all tasks.
- ### `GET /tasks/?status=pending` - Retrieve tasks filtered by status.
- ### `GET /tasks/?skip=0&limit=10` - Retrieve tasks with pagination.
- ### `GET /tasks/{task_id}` - Retrieve a specific task by ID.
- ### `PUT /tasks/{task_id}` - Update a specific task by ID.

```json
PUT /tasks/{
  task_id
}
Content-Type: application/json

{
"title": "New Name",
"due_date": "2025-00-00T15:00:00",
"status": "done"
}
```

Response:

```json
{
  "id": 1,
  "title": "New Name",
  "description": "Finish implementing the Task Manager",
  "text": "Add all features and test the system",
  "due_date": "2025-00-00T15:00:00",
  "status": "done",
  "celery_task_id": "abc123-def456-...",
  "created_at": "2025-00-00T00:00:00",
  "updated_at": "2025-00-00T01:00:00"
}
```

- ### `DELETE /tasks/{task_id}` - Delete a specific task by ID.
- ### `GET /health/` - Health check endpoint.

# Project Structure

## Backend

- `main.py` — Entry point for the FastAPI application.
- `config.py` — Configuration settings for the application.
- `models.py` — SQLAlchemy models for the database.
- `schemas.py` — Pydantic models for request and response validation.
- `crud.py` — CRUD operations for tasks.
- `database.py` — Database connection and session management.
- `celery_client.py` — Celery configuration and task definitions.
- `llm_client.py` — Integration with the language model API.

## Worker

- `celery_worker.py` — Entry point for the Celery worker.
- `config.py` — Configuration settings for the worker.
- `models.py` — SQLAlchemy models for the database.
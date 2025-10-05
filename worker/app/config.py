from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "..."
    REDIS_URL: str = "..."
    CELERY_BROKER_URL: str = "..."
    CELERY_RESULT_BACKEND: str = "..."

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_prefix: str = Field("/api/v1", validation_alias="API_PREFIX")
    database_url: str = Field("sqlite:///./dev.db", validation_alias="DATABASE_URL")
    redis_url: str = Field("redis://localhost:6379/0", validation_alias="REDIS_URL")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

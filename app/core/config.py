from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List
from functools import lru_cache

# DEBUG

# import pathlib
# DOTENV = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
# print("DOTENV PATH:", DOTENV)
# print("EXISTS:", pathlib.Path(DOTENV).exists())


class Settings(BaseSettings):
    SECRET_KEY: str = Field(...)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    RATE_LIMIT_PER_MINUTE: int = 60

    MODEL_PATH: str = "model.joblib"

    DATABASE_URL: str = "sqlite:///./data/users.db"

    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

if __name__ == "__main__":
    settings = get_settings()
    print(settings.SECRET_KEY)
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache
import json

class Settings(BaseSettings):
    SECRET_KEY: str = Field(...)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    RATE_LIMIT_PER_MINUTE: int = 60
    MODEL_PATH: str = "model.joblib"
    DATABASE_URL: str = "sqlite:///./data/users.db"

    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def allowed_origins_list(self) -> list[str]:
        v = self.ALLOWED_ORIGINS.strip()
        if v.startswith("[") and v.endswith("]"):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                pass
        return [s.strip().strip('"').strip("'") for s in v.split(",") if s.strip()]

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

if __name__ == "__main__":
    print(settings.allowed_origins_list)

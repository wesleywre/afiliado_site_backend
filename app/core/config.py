from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Promoções API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    POSTGRES_SERVER: str = "ep-jolly-truth-a5ncyrvu.us-east-2.aws.neon.tech"
    POSTGRES_USER: str = "afiliadodb_owner"
    POSTGRES_PASSWORD: str = "1mXOrPtB7NIu"
    POSTGRES_DB: str = "afiliadodb"

    DATABASE_URL: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    )

    # Segurança
    SECRET_KEY: str = "testesenha"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    class Config:
        env_file = ".env"


settings = Settings()

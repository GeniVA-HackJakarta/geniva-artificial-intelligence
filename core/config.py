import os
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    
    # PostgreSQL
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "mydb")

    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

    # Qdrant
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", 6333))
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME")
    QDRANT_EMBEDDING_NAME: str = os.getenv("QDRANT_EMBEDDING_NAME")
    QDRANT_LIMIT: int = int(os.getenv("QDRANT_LIMIT", 5))

    # Gemini
    GEMINI_MODEL_NAME: str = os.getenv("GEMINI_MODEL_NAME")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    GEMINI_TEMPERATURE: float = os.getenv("GEMINI_TEMPERATURE")
    GEMINI_VISION_MODEL_NAME: str = os.getenv("GEMINI_VISION_MODEL_NAME")

    # Gmaps
    GMAPS_API_KEY: str = os.getenv("GMAPS_API_KEY")

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    @property
    def QDRANT_URL(self):
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

config = Config()
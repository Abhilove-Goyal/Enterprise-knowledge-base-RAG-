from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "local"

    # Supabase (OPTIONAL)
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None

    # Paths
    DATA_PATH: str = Field(default="data/docs")
    INDEX_PATH: str = Field(default="index")

    # Ollama
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434")

    # Models
    EMBEDDING_MODEL: str = Field(default="nomic-embed-text")
    GENERATION_MODEL: str = Field(default="llama2")
    RERANK_MODEL: str = Field(default="phi3")
    INTENT_MODEL: str = Field(default="phi3")

    # Retrieval
    VECTOR_TOP_K: int = 30
    BM25_TOP_K: int = 30
    FINAL_TOP_K: int = 3

    # Chunking
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150

    # Evaluation
    ENABLE_EVALUATION: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


def get_settings():
    return Settings()

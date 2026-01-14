from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Paths
    SUPABASE_URL : str
    SUPABASE_KEY : str 
    DATA_PATH: str = Field(default="data/docs")
    INDEX_PATH: str = Field(default="index")
    LOG_PATH: str = Field(default="logs/interactions.jsonl")

    # Ollama
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434")
# for docker we use ollama:11434
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
    RERANK_MIN_SCORE: int = 3
    ENABLE_EVALUATION: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "forbid"


def get_settings():
    return Settings()

# Backwards-compatible single-instance settings object used across the project
# Some modules import `settings` directly, so provide it here.
settings = get_settings()

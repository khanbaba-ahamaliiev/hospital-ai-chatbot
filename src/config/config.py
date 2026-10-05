from pathlib import Path
import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

CONFIG_YAML = Path(__file__).resolve().parent / "config.yaml"

with open(CONFIG_YAML, "r", encoding="utf-8") as f:
    _raw_config = yaml.safe_load(f) or {}


class ModelConfig(BaseModel):
    name: str = "gemini-3.5-flash-lite"
    prompt_name: str = "system"


class RetrievalConfig(BaseModel):
    k: int = 3


class PineconeConfig(BaseModel):
    index_name: str = "hospital-chatbot"
    embedding_model: str = "gemini-embedding-001"
    dimension: int = 3072
    metric: str = "cosine"
    cloud: str = "aws"
    region: str = "us-east-1"
    min_pdf_chunk_chars: int = 50
    min_docx_chunk_chars: int = 80


class DatabaseConfig(BaseModel):
    sample_rows: int = 2
    max_query_results: int = 10


class ChatConfig(BaseModel):
    max_history_turns: int = 15


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    gemini_api_key: str = Field(alias="GEMINI_API_KEY")
    pinecone_api_key: str = Field(alias="PINECONE_API_KEY")
    supabase_url: str = Field(alias="SUPABASE_URL")

    model: ModelConfig
    retrieval: RetrievalConfig
    pinecone: PineconeConfig
    database: DatabaseConfig
    chat: ChatConfig


settings = Settings(**_raw_config)

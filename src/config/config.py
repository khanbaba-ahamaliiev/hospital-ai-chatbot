from pathlib import Path
import yaml
from pydantic import Field
from pydantic_settings import BaseSettings


CONFIG_YAML = Path(__file__).resolve().parent / "config.yaml"

with open(CONFIG_YAML, "r", encoding="utf-8") as f:
    _yaml_data = yaml.safe_load(f)

class Settings(BaseSettings):
    gemini_api_key: str = Field(alias="GEMINI_API_KEY")
    pinecone_api_key: str = Field(alias="PINECONE_API_KEY")
    supabase_url: str = Field(alias="SUPABASE_URL")
    
    model_name: str = _yaml_data["model"]["name"]
    retrieval_k: int = _yaml_data["retrieval"]["k"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True


settings = Settings()

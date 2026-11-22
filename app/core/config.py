from pydantic_settings import BaseSettings,SettingsConfigDict
from pathlib import Path
class Settings(BaseSettings):
    app_name:str
    api_v1_str:str
    database_url:str
    upload_dir: Path
    embedding_model:str
    gemini_api_key:str
    gemini_model:str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int 
    refresh_token_expire_days: int

    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings=Settings()
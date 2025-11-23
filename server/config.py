import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    DEBUG: bool = True

settings = Settings()

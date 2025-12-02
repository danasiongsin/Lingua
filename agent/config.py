import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration for the Language Learning Agent"""
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        return True

config = Config()

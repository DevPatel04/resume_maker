import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # LLM Settings
    MODEL_NAME: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000
    
    # Application Settings
    APP_NAME: str = "AI Resume Builder"
    DEBUG: bool = False
    
    # ATS Scoring Settings
    MIN_ATS_SCORE: int = 70
    KEYWORD_WEIGHT: float = 0.4
    FORMAT_WEIGHT: float = 0.3
    CONTENT_WEIGHT: float = 0.3
    
    class Config:
        env_file = ".env"

# Create global settings instance
settings = Settings()

# Validate required settings
if not settings.GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is required") 
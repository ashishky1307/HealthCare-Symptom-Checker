"""Core configuration settings."""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""
    
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Healthcare Symptom Checker API"
    VERSION: str = "1.0.0"
    
    # Server settings
    HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://healthcare_user:healthcare_password@localhost:5432/healthcare_db"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TTL: int = 3600
    
    # Groq LLM (Direct Integration)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
    
    # RAG Configuration
    RAG_ENABLED: bool = os.getenv("RAG_ENABLED", "True").lower() == "true"
    RAG_EMBEDDING_MODEL: str = os.getenv("RAG_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    RAG_TOP_K_RESULTS: int = int(os.getenv("RAG_TOP_K_RESULTS", "5"))
    RAG_MIN_RELEVANCE_SCORE: float = float(os.getenv("RAG_MIN_RELEVANCE_SCORE", "0.3"))
    RAG_MAX_CHUNKS_IN_CONTEXT: int = int(os.getenv("RAG_MAX_CHUNKS_IN_CONTEXT", "3"))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"


settings = Settings()

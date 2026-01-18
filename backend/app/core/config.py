"""
Core configuration management using Pydantic Settings.
All environment variables and application settings are defined here.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # API Keys
    gemini_api_key: str
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379"
    
    # Database Configuration
    database_url: str = "sqlite+aiosqlite:///./test.db"
    
    # Safety Limits
    query_timeout_seconds: int = 30
    max_rows: int = 10000
    
    # LLM Model Configuration
    classification_model: str = "gemini-1.5-flash"
    planning_model: str = "gemini-1.5-pro"
    
    # Cache Configuration
    cache_ttl_seconds: int = 3600
    schema_cache_permanent: bool = True
    
    # Feature Flags
    enable_query_logging: bool = True
    enable_insights: bool = True
    
    # SQL Safety - Keywords that should never be allowed
    SQL_FORBIDDEN_KEYWORDS: list[str] = [
        "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER",
        "TRUNCATE", "REPLACE", "MERGE", "GRANT", "REVOKE",
        "EXEC", "EXECUTE", "CALL"
    ]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

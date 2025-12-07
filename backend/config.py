"""
Configuration management using Pydantic Settings.
Loads environment variables from .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Supabase
    database_url: str
    supabase_url: str
    supabase_key: str
    
    # Discord
    discord_token: str
    discord_client_id: str
    discord_client_secret: str
    discord_redirect_uri: str = "http://localhost:3000/auth/callback"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_secret_key: str
    
    # Socket.IO
    socket_io_secret: str
    
    # AI (Optional)
    lm_studio_url: Optional[str] = "http://localhost:1234"
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"
    
    @property
    def cors_origins(self) -> list[str]:
        """Get CORS allowed origins based on environment."""
        if self.is_production:
            return [
                "https://your-domain.com",
                "https://www.your-domain.com"
            ]
        return [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173"
        ]


# Global settings instance
settings = Settings()


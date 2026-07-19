from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///data/conversations.db"
    SECRET_KEY: str = "change-me"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    AUTH_ISSUER: str = ""
    AUTH_CLIENT_ID: str = ""
    AUTH_CLIENT_SECRET: str = ""
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_WHATSAPP_NUMBER: str = ""
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: str = "http://localhost:8000,http://127.0.0.1:8000"
    OMS_API_BASE_URL: str = ""
    OMS_API_TOKEN: str = ""
    CATALOG_API_BASE_URL: str = ""
    CATALOG_API_TOKEN: str = ""
    RETURNS_API_BASE_URL: str = ""
    RETURNS_API_TOKEN: str = ""
    PROMOTIONS_API_BASE_URL: str = ""
    PROMOTIONS_API_TOKEN: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

@lru_cache()
def get_settings():
    return Settings()

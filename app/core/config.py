from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",  # explícito, aunque sea default
    )

    # 🔐 JWT
    JWT_PRIVATE_KEY_PATH: str
    JWT_PUBLIC_KEY_PATH: str
    JWT_ISSUER: str
    JWT_AUDIENCE: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    # 🌐 Backend (para armar links en correos)
    BACKEND_URL: str = "http://127.0.0.1:8000"


    # 🔐 2FA
    TWO_FA_ENCRYPTION_KEY: str

    # 🌐 Frontend
    FRONTEND_URL: str = "http://localhost:5500"

    # 📧 SMTP
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: str = "noreply@kiadez.com"
    SMTP_USE_SSL: bool = True
    SMTP_USE_TLS: bool = False

settings = Settings()

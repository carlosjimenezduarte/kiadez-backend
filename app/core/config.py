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

    # 🌐 CORS
    CORS_ALLOW_ORIGINS: str = (
        "http://localhost,"
        "http://127.0.0.1,"
        "http://localhost:5173,"
        "http://localhost:3000,"
        "https://kiadez.com,"
        "https://www.kiadez.com"
    )

    # 📧 SMTP
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: str = "noreply@kiadez.com"
    SMTP_USE_SSL: bool = True
    SMTP_USE_TLS: bool = False
    SUPPORT_EMAIL: str = "info@kiadez.com"

    # 🔑 Password reset
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 60

    # ☁️ S3 (Backblaze B2)
    S3_ENDPOINT: str
    S3_REGION: str
    S3_BUCKET: str
    S3_ACCESS_KEY_ID: str
    S3_SECRET_ACCESS_KEY: str
    S3_FORCE_PATH_STYLE: bool = True

    # 🎞️ Media
    MEDIA_UPLOAD_EXPIRE_MINUTES: int = 20
    MEDIA_DOWNLOAD_EXPIRE_HOURS: int = 24
    MEDIA_MAX_IMAGE_MB: int = 10
    MEDIA_MAX_VIDEO_MB: int = 100

settings = Settings()

from pydantic import model_validator
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

    # 🧪 Dev tools
    APP_ENV: str = "dev"

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
    # In dev/test these can be omitted to unblock local work that does not touch media uploads.
    # In production they are still enforced by validate_s3_for_environment.
    S3_ENDPOINT: str | None = None
    S3_REGION: str | None = None
    S3_BUCKET: str | None = None
    S3_ACCESS_KEY_ID: str | None = None
    S3_SECRET_ACCESS_KEY: str | None = None
    S3_FORCE_PATH_STYLE: bool = True

    # 🎞️ Media
    MEDIA_UPLOAD_EXPIRE_MINUTES: int = 20
    MEDIA_DOWNLOAD_EXPIRE_HOURS: int = 24
    MEDIA_MAX_IMAGE_MB: int = 10
    MEDIA_MAX_VIDEO_MB: int = 100

    @model_validator(mode="after")
    def validate_s3_for_environment(self):
        app_env = (self.APP_ENV or "").strip().lower()
        if app_env in {"prod", "production"}:
            required = {
                "S3_ENDPOINT": self.S3_ENDPOINT,
                "S3_REGION": self.S3_REGION,
                "S3_BUCKET": self.S3_BUCKET,
                "S3_ACCESS_KEY_ID": self.S3_ACCESS_KEY_ID,
                "S3_SECRET_ACCESS_KEY": self.S3_SECRET_ACCESS_KEY,
            }
            missing = [key for key, value in required.items() if not value]
            if missing:
                raise ValueError(
                    "Missing required S3 settings for production: "
                    + ", ".join(missing)
                )
        return self

settings = Settings()

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
    BACKEND_URL: str = "http://localhost:8000"

    # 🗄️ Database
    DATABASE_URL: str = (
        "postgresql+psycopg://kiadez_user:Kiadez_DB_Strong_2026!@localhost:5432/kiadez"
    )
    DB_ECHO: bool = False
    DB_POOL_PRE_PING: bool = True
    DB_POOL_SIZE: int = 4
    DB_MAX_OVERFLOW: int = 2
    DB_POOL_TIMEOUT_SECONDS: int = 30
    DB_POOL_RECYCLE_SECONDS: int = 1800

    # 🔐 2FA
    TWO_FA_ENCRYPTION_KEY: str

    # 🌐 Frontend
    FRONTEND_URL: str = "http://localhost:5500"

    # 🌐 CORS
    CORS_ALLOW_ORIGINS: str = (
        "http://localhost,"
        "http://localhost:5173,"
        "http://localhost:3000,"
        "https://kiadez.com,"
        "https://www.kiadez.com"
    )

    # 🧪 Dev tools
    APP_ENV: str = "dev"

    # 📧 Email provider
    EMAIL_PROVIDER: str = "smtp"  # smtp | mailgun
    EMAIL_SEND_TIMEOUT_SECONDS: int = 20

    # 📧 SMTP
    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_FROM: str = "noreply@kiadez.com"
    SMTP_USE_SSL: bool = True
    SMTP_USE_TLS: bool = False

    # 📧 Mailgun
    MAILGUN_API_BASE_URL: str = "https://api.mailgun.net/v3"
    MAILGUN_DOMAIN: str = "kiadez.com"
    MAILGUN_API_KEY: str | None = None
    MAILGUN_FROM: str = "Kiadez <noreply@kiadez.com>"

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

    # 💬 Messaging
    # Usernames/emails allowed to use "@allusers" broadcast in /messages/threads.
    # Comma-separated values, without @ for usernames.
    MESSAGES_BROADCAST_ALLOW_USERNAMES: str = "carlosjimenezd"
    MESSAGES_BROADCAST_ALLOW_EMAILS: str = ""

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

    @model_validator(mode="after")
    def validate_email_settings(self):
        provider = (self.EMAIL_PROVIDER or "smtp").strip().lower()
        if provider not in {"smtp", "mailgun"}:
            raise ValueError("EMAIL_PROVIDER must be either 'smtp' or 'mailgun'.")

        if self.EMAIL_SEND_TIMEOUT_SECONDS <= 0:
            raise ValueError("EMAIL_SEND_TIMEOUT_SECONDS must be a positive integer.")

        if provider == "smtp":
            required = {
                "SMTP_HOST": self.SMTP_HOST,
                "SMTP_PORT": self.SMTP_PORT,
                "SMTP_USER": self.SMTP_USER,
                "SMTP_PASSWORD": self.SMTP_PASSWORD,
            }
            missing = [key for key, value in required.items() if not value]
            if missing:
                raise ValueError(
                    "Missing required SMTP settings for EMAIL_PROVIDER=smtp: "
                    + ", ".join(missing)
                )
        else:
            required = {
                "MAILGUN_API_KEY": self.MAILGUN_API_KEY,
                "MAILGUN_DOMAIN": self.MAILGUN_DOMAIN,
            }
            missing = [key for key, value in required.items() if not value]
            if missing:
                raise ValueError(
                    "Missing required Mailgun settings for EMAIL_PROVIDER=mailgun: "
                    + ", ".join(missing)
                )

        return self

    @model_validator(mode="after")
    def validate_db_settings(self):
        if self.DB_POOL_SIZE <= 0:
            raise ValueError("DB_POOL_SIZE must be a positive integer.")
        if self.DB_MAX_OVERFLOW < 0:
            raise ValueError("DB_MAX_OVERFLOW must be zero or a positive integer.")
        if self.DB_POOL_TIMEOUT_SECONDS <= 0:
            raise ValueError("DB_POOL_TIMEOUT_SECONDS must be a positive integer.")
        if self.DB_POOL_RECYCLE_SECONDS < 0:
            raise ValueError("DB_POOL_RECYCLE_SECONDS must be zero or a positive integer.")
        return self

settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    JWT_PRIVATE_KEY_PATH: str
    JWT_PUBLIC_KEY_PATH: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    JWT_ISSUER: str = "kiadez"
    JWT_AUDIENCE: str = "kiadez-app"
    TWO_FA_ENCRYPTION_KEY: str  

settings = Settings()

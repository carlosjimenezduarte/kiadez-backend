from cryptography.fernet import Fernet
from app.core.config import settings


fernet = Fernet(settings.TWO_FA_ENCRYPTION_KEY.encode())


def encrypt_secret(secret: str) -> str:
    return fernet.encrypt(secret.encode()).decode()


def decrypt_secret(encrypted: str) -> str:
    return fernet.decrypt(encrypted.encode()).decode()

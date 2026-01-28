import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

AAD_VAULT = b"kiadez-vault-v1"
AAD_DESIRE = b"kiadez-private-desire-v1"
AAD_PURPOSE = b"kiadez-life-purpose-v1"

def derive_kek(password: str, salt: bytes) -> bytes:
    # Scrypt: robusto y práctico
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
    )
    return kdf.derive(password.encode("utf-8"))

def generate_dek() -> bytes:
    return os.urandom(32)

def wrap_dek(kek: bytes, dek: bytes) -> tuple[bytes, bytes]:
    aes = AESGCM(kek)
    nonce = os.urandom(12)
    wrapped = aes.encrypt(nonce, dek, AAD_VAULT)
    return nonce, wrapped

def unwrap_dek(kek: bytes, nonce: bytes, wrapped: bytes) -> bytes:
    aes = AESGCM(kek)
    return aes.decrypt(nonce, wrapped, AAD_VAULT)

def encrypt_with_dek(dek: bytes, plaintext: str, aad: bytes) -> tuple[bytes, bytes]:
    aes = AESGCM(dek)
    nonce = os.urandom(12)
    ct = aes.encrypt(nonce, plaintext.encode("utf-8"), aad)
    return nonce, ct

def decrypt_with_dek(dek: bytes, nonce: bytes, ciphertext: bytes, aad: bytes) -> str:
    aes = AESGCM(dek)
    pt = aes.decrypt(nonce, ciphertext, aad)
    return pt.decode("utf-8")

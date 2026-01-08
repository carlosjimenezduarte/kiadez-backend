from typing import Dict, Optional, Set
from .models import UserInternal

class InMemoryStore:
    def __init__(self) -> None:
        self._users_by_email: Dict[str, UserInternal] = {}
        self._users_by_number: Dict[int, UserInternal] = {}
        self._next_user_number: int = 0

        # Allowlist de refresh JTIs (sin DB, esto se pierde al reiniciar)
        self._refresh_jtis: Set[str] = set()

    def create_user(self, email: str, password_hash: str, role: str = "user") -> UserInternal:
        if email.lower() in self._users_by_email:
            raise ValueError("Email ya registrado.")

        user_number = self._next_user_number
        self._next_user_number += 1

        user = UserInternal(
            user_number=user_number,
            email=email.lower(),
            role=role,                # arranca en "user" (o el que decidas)
            guardian_rank=None,       # NULL al inicio (ganado después)
            is_active=True,
            password_hash=password_hash,
        )

        self._users_by_email[user.email] = user
        self._users_by_number[user.user_number] = user
        return user

    def get_user_by_email(self, email: str) -> Optional[UserInternal]:
        return self._users_by_email.get(email.lower())

    def get_user_by_number(self, user_number: int) -> Optional[UserInternal]:
        return self._users_by_number.get(user_number)

    def add_refresh_jti(self, jti: str) -> None:
        self._refresh_jtis.add(jti)

    def has_refresh_jti(self, jti: str) -> bool:
        return jti in self._refresh_jtis

    def revoke_refresh_jti(self, jti: str) -> None:
        self._refresh_jtis.discard(jti)

store = InMemoryStore()

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user_2fa import User2FA


class User2FARepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_user_id(self, user_id: int) -> User2FA | None:
        stmt = select(User2FA).where(User2FA.user_id == user_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def create(self, user_id: int, secret_encrypted: str) -> User2FA:
        obj = User2FA(
            user_id=user_id,
            secret_encrypted=secret_encrypted,
            is_enabled=False,
        )
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def enable(self, obj: User2FA) -> None:
        obj.is_enabled = True
        self.session.commit()

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, email: str, password_hash: str, role: str = "user") -> User:
        user = User(
            email=email.lower(),
            password_hash=password_hash,
            role=role,
            guardian_rank=None,
            is_active=True,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email.lower())
        return self.session.execute(stmt).scalar_one_or_none()

    def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return self.session.execute(stmt).scalar_one_or_none()

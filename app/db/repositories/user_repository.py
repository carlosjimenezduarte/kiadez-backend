from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user import User
from datetime import date

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(
        self,
        *,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str,
        birth_date: date,
        gender: str,
        role: str = "user",
        is_active: bool = True,
    ) -> User:
        user = User(
            email=email.lower(),
            password_hash=password_hash,
            role=role,
            guardian_rank=None,
            is_active=is_active,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            gender=gender,
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

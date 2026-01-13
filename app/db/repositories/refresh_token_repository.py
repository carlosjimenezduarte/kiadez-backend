from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, *, user_id: int, jti: str, expires_at: datetime) -> RefreshToken:
        token = RefreshToken(
            user_id=user_id,
            jti=jti,
            expires_at=expires_at,
        )
        self.session.add(token)
        self.session.commit()
        self.session.refresh(token)
        return token

    def get_valid(self, jti: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(
            RefreshToken.jti == jti,
            RefreshToken.is_revoked.is_(False),
            RefreshToken.expires_at > datetime.now(timezone.utc),
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def revoke(self, token: RefreshToken) -> None:
        token.is_revoked = True
        self.session.commit()

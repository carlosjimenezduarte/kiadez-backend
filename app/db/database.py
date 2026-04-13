from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=bool(settings.DB_ECHO),
    future=True,
    pool_pre_ping=bool(settings.DB_POOL_PRE_PING),
    pool_size=max(1, int(settings.DB_POOL_SIZE)),
    max_overflow=max(0, int(settings.DB_MAX_OVERFLOW)),
    pool_timeout=max(1, int(settings.DB_POOL_TIMEOUT_SECONDS)),
    pool_recycle=max(0, int(settings.DB_POOL_RECYCLE_SECONDS)),
    pool_use_lifo=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

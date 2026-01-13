"""from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = (
    "postgresql+psycopg://kiadez_user:Kiadez_DB_Strong_2026!"
    "@localhost:5432/kiadez"
)

class Base(DeclarativeBase):
    pass

engine = create_engine(
    DATABASE_URL,
    echo=False,        # luego puedes poner True si quieres ver SQL
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql+psycopg://kiadez_user:Kiadez_DB_Strong_2026!@localhost:5432/kiadez"

engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

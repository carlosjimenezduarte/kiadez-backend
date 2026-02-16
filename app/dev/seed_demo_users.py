from __future__ import annotations

from datetime import date

from sqlalchemy import select

from app.core.security import hash_password
from app.db.database import SessionLocal
from app.db.models.user import User


DEMO_USERS = [
    {
        "first_name": "Carlos",
        "last_name": "Jimenez Duarte",
        "email": "carlos.demo@example.com",
        "birth_date": date(1986, 1, 15),
        "gender": "male",
        "password": "CarlosDemo*2026",
        "role": "guardian",
        "guardian_rank": 1,
        "username": "carlosjimenezduarte",
    },
    {
        "first_name": "David",
        "last_name": "Jimenez Florez",
        "email": "david.demo@example.com",
        "birth_date": date(1990, 4, 20),
        "gender": "male",
        "password": "DavidDemo*2026",
        "role": "user",
        "guardian_rank": None,
        "username": "davidjimenezflorez",
    },
]


def upsert_demo_users() -> None:
    db = SessionLocal()
    try:
        for payload in DEMO_USERS:
            email = payload["email"].strip().lower()
            stmt = select(User).where(User.email == email)
            user = db.execute(stmt).scalar_one_or_none()

            if user is None:
                user = User(
                    first_name=payload["first_name"],
                    last_name=payload["last_name"],
                    email=email,
                    birth_date=payload["birth_date"],
                    gender=payload["gender"],
                    password_hash=hash_password(payload["password"]),
                    role=payload["role"],
                    guardian_rank=payload["guardian_rank"],
                    username=payload["username"],
                    is_active=True,
                )
                db.add(user)
            else:
                user.first_name = payload["first_name"]
                user.last_name = payload["last_name"]
                user.birth_date = payload["birth_date"]
                user.gender = payload["gender"]
                user.password_hash = hash_password(payload["password"])
                user.role = payload["role"]
                user.guardian_rank = payload["guardian_rank"]
                user.username = payload["username"]
                user.is_active = True

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    upsert_demo_users()
    print("Demo users ready:")
    for payload in DEMO_USERS:
        print(f"- {payload['email']} | password: {payload['password']} | role: {payload['role']}")

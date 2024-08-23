import random

from sqlalchemy.orm import Session

from app.api.v1.auth.models import User


def create_basic_user(dbsession: Session) -> tuple:

    password = "test1234"

    user = User(
        email=f"test{random.randint(0, 1000)}@test.com",
        name="test",
        password=password,
    )

    dbsession.add(user)
    dbsession.commit()

    return user, password

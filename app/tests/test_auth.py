from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app.tests.utils import create_basic_user


def test_signup(client: TestClient, dbsession: Session):
    response = client.post(
        "/v1/auth/signup",
        json={
            "email": "test@test.com",
            "password": "tes12341234",
            "name": "test",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == "test@test.com"


def test_login(client: TestClient, dbsession: Session):

    user, password = create_basic_user(dbsession)

    response = client.post(
        "/v1/auth/login",
        json={
            "email": user.email,
            "password": password,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == user.email

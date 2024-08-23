from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status


def test_send_message(
    fastapi_app: FastAPI,
    user_client: TestClient,
    dbsession: Session,
):

    url = fastapi_app.url_path_for("send_message")

    response = user_client.post(
        url,
        json={
            "message": "Hello, world!",
        },
    )

    assert response.status_code == status.HTTP_200_OK

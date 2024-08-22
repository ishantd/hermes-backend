from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status


def test_base():
    # very basic one test
    assert 1 == 1


def test_health_check(client: TestClient, dbsession: Session):

    response = client.get("/v1/health/")

    assert response.status_code == status.HTTP_200_OK
    assert "OK" in response.text

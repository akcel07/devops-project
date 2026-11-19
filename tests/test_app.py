import pytest

from app import create_app


@pytest.fixture
def client():
    return create_app().test_client()


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_visits_increments(client):
    assert client.get("/visits").get_json() == {"visits": 1}
    assert client.get("/visits").get_json() == {"visits": 2}
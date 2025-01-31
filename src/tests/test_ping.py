import pytest
from starlette.testclient import TestClient
from app.main import app

@pytest.fixture
def test_app():
    client = TestClient(app)
    yield client

def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
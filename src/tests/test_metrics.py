# test for the prometheues metrics endpoint 
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import notes, database
from app.api.models import NoteSchema
from datetime import datetime as dt
from app.api import crud

client = TestClient(app)


@pytest.fixture(scope="module")
def test_app():
    # setup
    yield client
    # teardown
    database.disconnect()


def test_create_note_invalid_json(test_app):
    response = test_app.post("/notes/", data=json.dumps({"title": "something"}))
    assert response.status_code == 422
    response = test_app.post("/notes/", data=json.dumps({"title": "1", "description": "2"}))
    assert response.status_code == 422


def test_create_note_invalid_json_keys(test_app):
    response = test_app.post("/notes/", data=json.dumps({"title": "1", "description": "2", "completed": False}))
    assert response.status_code == 422
    response = test_app.post("/notes/", data=json.dumps({"name": "something"}))
    assert response.status_code == 422

def test_read_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notes/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

def test_read_note_invalid_id(test_app):
    response = test_app.get("/notes/one/")
    assert response.status_code == 422

def test_read_notes(test_app, monkeypatch):
    test_data = [
        {"id": 1, "title": "something", "description": "something else", "completed": "False", "created_date": dt.now().strftime("%Y-%m-%d %H:%M")},
        {"id": 2, "title": "someone", "description": "someone else", "completed": "False", "created_date": dt.now().strftime("%Y-%m-%d %H:%M")},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/notes/")
    assert response.status_code == 200
    assert response.json() == test_data

# prometheus metrics endpoint test

def test_metrics(test_app):
    response = test_app.get("/metrics")
    assert response.status_code == 200

def test_metrics_invalid_path(test_app):
    response = test_app.get("/metrics/invalid")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

def test_metrics_invalid_method(test_app):
    response = test_app.post("/metrics")
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"

def test_metrics_get_request(test_app):
    response = test_app.get("/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; version=0.0.4; charset=utf-8"

def test_metrics_post_request(test_app):
    response = test_app.post("/metrics")
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"

def test_metrics_put_request(test_app):
    response = test_app.put("/metrics")
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"

def test_metrics_delete_request(test_app):
    response = test_app.delete("/metrics")
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"


def test_metrics_patch_request(test_app):
    response = test_app.patch("/metrics")
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"

def test_metrics_options_request(test_app):
    response = test_app.options("/metrics")
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"



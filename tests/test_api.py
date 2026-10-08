import os

os.environ["API_KEY"] = "test-key"

import pytest  # noqa: E402

from app import create_app  # noqa: E402


@pytest.fixture
def client():
    app = create_app(testing=True)
    with app.test_client() as c:
        yield c


@pytest.fixture
def auth_headers():
    return {"X-API-KEY": "test-key", "Content-Type": "application/json"}


def test_homepage(client):
    resp = client.get("/app")
    assert resp.status_code == 200
    assert b"User Registration CRUD" in resp.data


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "healthy"


def test_list_users_empty(client):
    resp = client.get("/api/")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_user_unauthorized(client):
    resp = client.post("/api/", json={
        "username": "john", "email": "john@example.com", "full_name": "John Doe"
    })
    assert resp.status_code == 401


def test_create_user(client, auth_headers):
    resp = client.post("/api/", json={
        "username": "john", "email": "john@example.com", "full_name": "John Doe"
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["username"] == "john"
    assert data["email"] == "john@example.com"


def test_get_user(client, auth_headers):
    client.post("/api/", json={
        "username": "jane", "email": "jane@example.com", "full_name": "Jane Doe"
    }, headers=auth_headers)

    resp = client.get("/api/1")
    assert resp.status_code == 200
    assert resp.get_json()["username"] == "jane"


def test_get_user_not_found(client):
    resp = client.get("/api/999")
    assert resp.status_code == 404


def test_update_user(client, auth_headers):
    client.post("/api/", json={
        "username": "bob", "email": "bob@example.com", "full_name": "Bob"
    }, headers=auth_headers)

    resp = client.put("/api/1", json={
        "username": "bob_updated", "email": "bob2@example.com", "full_name": "Bob Updated"
    }, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["username"] == "bob_updated"


def test_delete_user(client, auth_headers):
    client.post("/api/", json={
        "username": "charlie", "email": "charlie@example.com", "full_name": "Charlie"
    }, headers=auth_headers)

    resp = client.delete("/api/1", headers=auth_headers)
    assert resp.status_code == 204

    resp = client.get("/api/1")
    assert resp.status_code == 404


def test_create_user_invalid_email(client, auth_headers):
    resp = client.post("/api/", json={
        "username": "bad", "email": "not-an-email", "full_name": "Bad User"
    }, headers=auth_headers)
    assert resp.status_code == 400


def test_create_user_missing_fields(client, auth_headers):
    resp = client.post("/api/", json={
        "username": "incomplete"
    }, headers=auth_headers)
    assert resp.status_code == 400

import pytest

def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200

def test_login_invalid_credentials(client):
    response = client.post("/login", data={
        "username": "admin",
        "password": "wrong"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"invalid" in response.data.lower() or b"error" in response.data.lower()

def test_login_missing_fields(client):
    response = client.post("/login", data={}, follow_redirects=True)
    assert response.status_code == 200
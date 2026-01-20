import pytest

def test_login_valid_credentials(client):
    """Test login with valid credentials"""
    response = client.post("/login", data={
        "username": "admin",
        "password": "password"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"logged in" in response.data or b"dashboard" in response.data

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post("/login", data={
        "username": "admin",
        "password": "wrongpassword"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"invalid" in response.data.lower() or b"error" in response.data.lower()

def test_login_required_fields(client):
    """Test login with missing fields"""
    response = client.post("/login", data={}, follow_redirects=True)
    assert response.status_code == 200 or response.status_code == 400
import io
import os
import pytest
from sample_app import sample

@pytest.fixture
def client():
    sample.config["TESTING"] = True
    upload_dir = os.path.join("static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    with sample.test_client() as client:
        yield client

@pytest.fixture
def sample_image():
    """Fixture providing a sample image file"""
    return (io.BytesIO(b"fake image data"), "sample.jpg")

@pytest.fixture
def authenticated_client(client):
    """Fixture for authenticated client session"""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['username'] = 'testuser'
    return client
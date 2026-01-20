import os
import pytest
from sample_app import sample

@pytest.fixture
def client():
    sample.config["TESTING"] = True

    # Ensure upload directory exists for tests
    upload_dir = os.path.join("static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    with sample.test_client() as client:
        yield client

import pytest
from sample_app import sample

@pytest.fixture
def client():
    """
    Provides a Flask test client
    """
    sample.config["TESTING"] = True
    with sample.test_client() as client:
        yield client

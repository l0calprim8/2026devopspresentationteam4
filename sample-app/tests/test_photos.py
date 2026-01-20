import io
import pytest

def test_homepage_no_images(client):
    """
    GIVEN no images in session
    WHEN accessing "/"
    THEN gallery should be empty
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b'<div class="grid' not in response.data


def test_upload_single_image(client):
    """
    GIVEN a single image file
    WHEN POST to "/upload"
    THEN image is added to session
    """
    data = {
        "images": (io.BytesIO(b"fake image data"), "test1.jpg")
    }

    response = client.post("/upload", data=data, content_type="multipart/form-data", follow_redirects=True)
    assert response.status_code == 200
    assert b'test1.jpg' in response.data  # Placeholder: adjust after template rendering


def test_upload_multiple_images(client):
    """
    GIVEN multiple image files
    WHEN POST to "/upload"
    THEN all images are added to session
    """
    data = {
        "images": [
            (io.BytesIO(b"image1"), "img1.jpg"),
            (io.BytesIO(b"image2"), "img2.jpg"),
        ]
    }

    response = client.post("/upload", data=data, content_type="multipart/form-data", follow_redirects=True)
    assert response.status_code == 200
    assert b'img1.jpg' in response.data
    assert b'img2.jpg' in response.data


def test_upload_no_file(client):
    """
    GIVEN no file submitted
    WHEN POST to "/upload"
    THEN redirect to home and no images added
    """
    response = client.post("/upload", data={}, follow_redirects=True)
    assert response.status_code == 200
    assert b'<div class="grid' not in response.data


def test_intentional_failure_demo():
    """
    This test is used to demonstrate
    CI/CD pipeline failure when code breaks
    """
    assert False

import io
import os
import shutil
import pytest
from sample_app import sample

IMAGES_DB = "uploads/images.txt"
UPLOAD_FOLDER = "uploads"


# Automatically clear images database and folder before each test
@pytest.fixture(autouse=True)
def clear_images_file():
    # Ensure uploads folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Clear images.txt
    open(IMAGES_DB, "w").close()
    
    # Remove any files in uploads folder
    for f in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, f)
        if os.path.isfile(file_path):
            os.remove(file_path)


@pytest.fixture
def client():
    """Provides a Flask test client for unauthenticated tests."""
    sample.config["TESTING"] = True
    with sample.test_client() as client:
        with client.session_transaction() as sess:
            sess.clear()
        yield client


@pytest.fixture
def authenticated_client(client):
    """Provides a Flask test client with a logged-in session."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['username'] = 'testuser'
    return client


@pytest.fixture
def sample_image():
    """Fixture providing a sample image file."""
    return (io.BytesIO(b"fake image data"), "sample.jpg")


# ---------------------------
# Fixtures for future delete tests
# ---------------------------

# @pytest.fixture
# def single_uploaded_image(authenticated_client, sample_image):
#     """Upload one image to test single deletion."""
#     data = {'images': sample_image}
#     authenticated_client.post("/upload", data=data, content_type="multipart/form-data")
#     return sample_image[1]  # filename

# @pytest.fixture
# def multiple_uploaded_images(authenticated_client):
#     """Upload multiple images to test multiple deletion."""
#     images = [
#         (io.BytesIO(b"image1"), "img1.jpg"),
#         (io.BytesIO(b"image2"), "img2.jpg")
#     ]
#     for img in images:
#         authenticated_client.post("/upload", data={'images': img}, content_type="multipart/form-data")
#     return [img[1] for img in images]  # list of filenames
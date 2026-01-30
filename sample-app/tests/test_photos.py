import os
import io
import pytest
from sample_app import IMAGES_DB, UPLOAD_FOLDER


def test_homepage_no_images(client):
    """
    GIVEN no images uploaded
    WHEN accessing "/"
    THEN gallery should be empty
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b'<div class="grid' not in response.data


def test_upload_single_image(authenticated_client, sample_image):
    """
    GIVEN logged-in user uploads a single image
    WHEN POST to "/upload"
    THEN image is added to gallery
    """
    file_data, filename = sample_image
    response = authenticated_client.post(
        "/upload",
        data={"images": (file_data, filename)},
        content_type="multipart/form-data",
        follow_redirects=True
    )
    assert response.status_code == 200
    assert bytes(filename, "utf-8") in response.data

    # Clean up
    uploaded_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(uploaded_path):
        os.remove(uploaded_path)


def test_upload_multiple_images(authenticated_client):
    """
    GIVEN logged-in user uploads multiple images
    WHEN POST to "/upload"
    THEN images are added to gallery
    """
    files = [
        (io.BytesIO(b"image1"), "img1.jpg"),
        (io.BytesIO(b"image2"), "img2.jpg")
    ]

    # Correct way: dictionary mapping field name to a list of files
    data = {
        "images": files
    }

    response = authenticated_client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True
    )

    assert response.status_code == 200
    for _, filename in files:
        assert bytes(filename, "utf-8") in response.data

        # Clean up uploaded files
        uploaded_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(uploaded_path):
            os.remove(uploaded_path)


def test_upload_no_file(authenticated_client):
    """
    GIVEN logged-in user submits no files
    WHEN POST to "/upload"
    THEN no images are added
    """
    response = authenticated_client.post(
        "/upload",
        data={},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'<div class="grid' not in response.data

    # Commented-out tests for future delete functionality

# @pytest.mark.skip(reason="Delete endpoint not implemented yet")
# def test_delete_single_image(authenticated_client, sample_image, clear_images_file):
#     """
#     GIVEN a logged-in user with one uploaded image
#     WHEN DELETE to "/delete/<filename>"
#     THEN the image is removed from the gallery
#     """
#     # Upload the image first
#     authenticated_client.post(
#         "/upload",
#         data={"images": sample_image},
#         content_type="multipart/form-data",
#         follow_redirects=True
#     )
#     
#     # Delete the image
#     filename = sample_image[1]
#     response = authenticated_client.post(
#         f"/delete/{filename}",
#         follow_redirects=True
#     )
#     
#     assert response.status_code == 200
#     # Gallery should now be empty
#     assert b'<div class="grid' not in response.data
#
# @pytest.mark.skip(reason="Delete endpoint not implemented yet")
# def test_delete_multiple_images(authenticated_client, clear_images_file):
#     """
#     GIVEN a logged-in user with multiple uploaded images
#     WHEN DELETE to "/delete" with a list of filenames
#     THEN all specified images are removed from the gallery
#     """
#     # Upload multiple images
#     files = [
#         (io.BytesIO(b"image1"), "img1.jpg"),
#         (io.BytesIO(b"image2"), "img2.jpg")
#     ]
#     data = [("images", file) for file in files]
#     authenticated_client.post(
#         "/upload",
#         data=data,
#         content_type="multipart/form-data",
#         follow_redirects=True
#     )
#     
#     # Delete multiple images
#     filenames_to_delete = ["img1.jpg", "img2.jpg"]
#     response = authenticated_client.post(
#         "/delete",
#         data={"filenames": filenames_to_delete},
#         follow_redirects=True
#     )
#     
#     assert response.status_code == 200
#     # Gallery should now be empty
#     assert b'<div class="grid' not in response.data
from http import HTTPStatus
from .helpers import helpers


def test_upload__success(client):
    image = helpers.load_binary_file("kitty.jpg")
    response = client.post(
        "/", data={"image": image}, content_type="multipart/form-data"
    )
    assert response.status_code  # == 200


def test_upload__with_missing_file(client):
    response = client.post("/", data={}, content_type="multipart/form-data")

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_upload__with_invalid_mime_type(client):
    image = helpers.load_file_data("bad_kitty.gif")
    response = client.post(
        "/", data={"image": image}, content_type="multipart/form-data"
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST

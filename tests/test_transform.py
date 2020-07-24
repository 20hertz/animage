from http import HTTPStatus
from .helpers import helpers

GRAYSCALE_ENDPOINT = "/grayscale"


def test_upload__success(client):
    image = helpers.load_file_data("kitty.jpg")
    response = client.post(
        GRAYSCALE_ENDPOINT, data={"image": image}, content_type="multipart/form-data"
    )
    assert response.status_code == HTTPStatus.OK


def test_upload__with_missing_file(client):
    response = client.post(
        GRAYSCALE_ENDPOINT, data={}, content_type="multipart/form-data"
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_upload__with_invalid_mime_type(client):
    image = helpers.load_file_data("bad_kitty.gif")
    response = client.post(
        GRAYSCALE_ENDPOINT, data={"image": image}, content_type="multipart/form-data"
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST

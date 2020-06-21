from .helpers import helpers


def test_root__success(client):
    image = helpers.load_binary_file("kitty.jpg")

    response = client.post(
        "/", data={"image": image}, content_type="multipart/form-data"
    )
    assert response.status_code == 200

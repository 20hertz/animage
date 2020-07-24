# import pytest
# from flask import Flask


# @pytest.fixture()
# def app() -> Flask:
#     from app import create_app

#     return create_app()


# import pytest

# from app import create_app


# @pytest.fixture
# def app():
#     app = create_app()
#     return app.app


import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client

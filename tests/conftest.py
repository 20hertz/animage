import pytest
from flask import Flask
from app import create_app


@pytest.fixture
def app() -> Flask:
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client

import pytest
from flask import Flask


@pytest.fixture()
def app() -> Flask:
    from app import create_app

    return create_app()

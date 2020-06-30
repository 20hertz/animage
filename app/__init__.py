from flask import Flask
import flask_cors
import os
from .config import CONFIGS

CONFIG_NAME = os.getenv("FLASK_ENV")


def create_app(config_name):
    app = Flask(__name__)
    flask_cors.CORS(app)
    app.config.from_object(CONFIGS[config_name])

    register_blueprint(app)

    return app


def register_blueprint(app):
    from app.service.transform import transform_blueprint

    app.register_blueprint(transform_blueprint)


app = create_app(CONFIG_NAME)

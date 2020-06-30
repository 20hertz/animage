from flask import Flask
import flask_cors
from .config import CONFIGS


def create_app(config_name):
    app = Flask(__name__)
    flask_cors.CORS(app)
    app.config.from_object(CONFIGS["development"])

    register_blueprint(app)

    return app


def register_blueprint(app):
    from app.service.transform import transform_blueprint

    app.register_blueprint(transform_blueprint)

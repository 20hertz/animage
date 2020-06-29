from flask import Flask
import flask_cors

from .config import configs


def create_app(env):
    app = Flask(__name__)
    flask_cors.CORS(app)
    app.config.from_object(configs[env])
    app.config["CORS_HEADERS"] = "Content-Type"

    register_blueprint(app)

    return app


def register_blueprint(app):
    from app.service.transform import transform_blueprint

    app.register_blueprint(transform_blueprint)

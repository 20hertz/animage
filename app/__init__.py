from flask import Flask
from flask_cors import CORS

from .config import configs


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(configs[env])
    CORS(
        app,
        resources={
            r"/": {
                "origins": [
                    "http://localhost:1234",
                    "https://d289aztbzuse4k.cloudfront.net",
                ]
            }
        },
    )
    register_blueprint(app)

    return app


def register_blueprint(app):
    from app.service.transform import transform_blueprint

    app.register_blueprint(transform_blueprint)

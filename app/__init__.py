from flask import Flask
import flask_cors
import os


def create_app() -> Flask:

    from .config import config_by_name

    app = Flask(__name__)

    CONFIG_NAME = os.getenv("FLASK_ENV", "development")
    app.logger.debug(f"Config name is: {CONFIG_NAME}")
    config = config_by_name[CONFIG_NAME]
    app.config.from_object(config)
    flask_cors.CORS(
        app, resources={r"/*": {"origins": app.config["ALLOWED_ORIGINS"]}},
    )

    register_blueprint(app)

    return app


def register_blueprint(app):
    from app.service.transform import transform_blueprint

    app.register_blueprint(transform_blueprint)

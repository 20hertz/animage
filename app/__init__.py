from flask import Flask


from .config import configs


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(configs[env])

    register_blueprint(app)

    return app


def register_blueprint(app):
    from app.service.transform import transform_blueprint

    app.register_blueprint(transform_blueprint)

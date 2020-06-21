import os

from app import create_app


application = create_app(os.getenv("FLASK_ENV"))

if __name__ == "__main__":
    application.run()

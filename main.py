from flask import Flask
from src.routes import configure_routes

UPLOAD_FOLDER = '/tmp'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

configure_routes(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

from flask import Flask
from src.routes import configure_routes
from flask_cors import CORS

app = Flask(__name__)

if app.config['ENV'] == 'staging':
    app.config.from_object('config.StagingConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

cors = CORS(app, resources={
    r"/": {
        "origins": ["http://localhost:1234", "https://d289aztbzuse4k.cloudfront.net"]
    }
})


configure_routes(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)

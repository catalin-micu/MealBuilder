from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    from .route.dummy_route import dummy_api
    app.register_blueprint(dummy_api)

    return app

from flask import Flask
from flask_cors import CORS
from flask_server.route import BLUEPRINTS


def create_app():
    app = Flask(__name__)
    CORS(app)

    # from .route.dummy_route import dummy_api
    # app.register_blueprint(dummy_api)

    for bp in BLUEPRINTS:
        app.register_blueprint(blueprint=bp)

    return app

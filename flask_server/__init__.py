from flask import Flask
from flask_cors import CORS
from flask_server.route import BLUEPRINTS


def create_app():
    """
    creates core flask app and automatically registers all blueprints available
    :return: runnable flask app object
    """
    app = Flask(__name__)
    CORS(app)

    for bp in BLUEPRINTS:
        app.register_blueprint(blueprint=bp)

    return app

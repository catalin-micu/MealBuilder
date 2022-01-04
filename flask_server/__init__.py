from flask import Flask
from flask_cors import CORS
from flask_server.route import BLUEPRINTS


def create_app():
    app = Flask(__name__)
    CORS(app)

    # sterge asta

    for bp in BLUEPRINTS:
        app.register_blueprint(blueprint=bp)

    return app

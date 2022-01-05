import logging
from flask import Flask
from flask_cors import CORS
from flask_server.route import BLUEPRINTS


def create_logger(name: str, form: str):
    """
    creates custom logger object
    :param name: name of the logger (convention to use __name__ when the function is called)
    :param form: shape of the logged messages
    :return: logger object
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(form)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


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

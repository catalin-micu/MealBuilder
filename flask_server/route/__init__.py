"""maybe we will use this"""
from flask_server.route.dummy_route import dummy_api
from flask_server.route.users import users_blueprint

BLUEPRINTS = {dummy_api, users_blueprint}

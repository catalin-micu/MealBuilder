"""maybe we will use this"""
from flask_server.route.calories_calculator import calories_calculator_blueprint
from flask_server.route.dashboard import dashboard_blueprint
from flask_server.route.dummy_route import dummy_api
from flask_server.route.restaurants import restaurants_blueprint
from flask_server.route.users import users_blueprint
from flask_server.route.stripe import stripe_blueprint

BLUEPRINTS = {dummy_api, users_blueprint, restaurants_blueprint, dashboard_blueprint, calories_calculator_blueprint,
              stripe_blueprint}

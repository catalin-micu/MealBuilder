from flask import Blueprint, request, Response, jsonify
from flask_server.model.restaurants import Restaurants
from flask_server.model.users import Users

dashboard_blueprint = Blueprint('dashboard_blueprint', __name__, url_prefix='/dashboard')
users = Users()
restaurants = Restaurants()


@dashboard_blueprint.route('/nearby-restaurants', methods=['POST'])
def get_nearby_restaurants():
    target_city = request.json.get('city')
    restaurants_list = restaurants.get_restaurants_in_given_city(target_city)
    if len(restaurants_list) == 0:
        return Response(f"No restaurants for city '{target_city}'", status=404)
    return jsonify(restaurants_list)


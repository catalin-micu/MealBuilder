from flask import Blueprint, request, Response, jsonify
from flask_server.model.restaurants import Restaurants
from flask_server.model.users import Users
from flask_jwt_extended import jwt_required

dashboard_blueprint = Blueprint('dashboard_blueprint', __name__, url_prefix='/dashboard')
users = Users()
restaurants = Restaurants()


@dashboard_blueprint.route('/cities-for-logged-user', methods=['POST'])
@jwt_required
def get_addresses():
    email = request.json.get('email')
    if not email:
        return Response("no email in request body", status=404)
    addresses = users.get_user_data_from_email(email).get('preferred_addresses')

    return jsonify([item.get('city') for item in addresses])


@dashboard_blueprint.route('/nearby-restaurants', methods=['POST'])
@jwt_required
def get_nearby_restaurants():
    """
    gets all the restaurants in a particular city
    :return: list of dicts with data about the restaurants in that city (keys mapped to table column names)
    {
        "city": "bucuresti"
    }
    """
    target_city = request.json.get('city')
    if not target_city:
        return Response("no email in request body", status=404)

    restaurants_list = restaurants.get_restaurants_in_given_city(target_city)
    if len(restaurants_list) == 0:
        return Response(f"No restaurants for city '{target_city}'", status=404)
    return jsonify(restaurants_list)


@dashboard_blueprint.route('/search-restaurants', methods=['POST'])
@jwt_required
def search_restaurants():
    """
    gets restaurant based on name
    :return: list of dicts with data about the restaurants in that city (keys mapped to table column names)
    {
        "name": "la arabi"
    }
    """
    restaurant_name_input = request.json.get('name')
    restaurants_list = restaurants.search_restaurants_by_name(restaurant_name_input)
    if len(restaurants_list) == 0:
        return Response(f"No restaurants like '{restaurant_name_input}'", status=404)
    return jsonify(restaurants_list[0])

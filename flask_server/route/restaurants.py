from flask import Blueprint, request
from flask_server.model.restaurants import Restaurants

restaurants_blueprint = Blueprint('restaurants_blueprint', __name__, url_prefix='/restaurants')


@restaurants_blueprint.route('/upsert_from_code', methods=['POST'])
def upsert_from_code():
    data = request.json
    restaurants = Restaurants()
    restaurants.upsert_row(rows=data)

    return '200'


@restaurants_blueprint.route('/upsert_from_file', methods=['POST'])
def upsert_from_file():
    file_path = request.json.get('filePath')
    restaurants = Restaurants()
    restaurants.batch_upsert(file_path)

    return '200'

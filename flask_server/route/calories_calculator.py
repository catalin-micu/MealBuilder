import json

from flask import Blueprint, request, Response, jsonify

from flask_server import utils
from flask_server.model.products import Products
from flask_server.model.restaurants import Restaurants

calories_calculator_blueprint = Blueprint('calories_calculator_blueprint', __name__, url_prefix='/calories-calculator')
REQUIRED_PARAMS_FOR_DAILY_CALORIES = {'weight', 'height', 'age', 'gender', 'activity'}


def validate_request_data_for_daily_calories(data: dict) -> bool:
    for param in REQUIRED_PARAMS_FOR_DAILY_CALORIES:
        if param not in list(data.keys()):
            return False
    return True


@calories_calculator_blueprint.route('/calculate-caloric-needs-per-day', methods=['POST'])
def calculate_daily_calories():
    data = request.json
    if not validate_request_data_for_daily_calories(data):
        return Response(f"Invalid params for daily calories calculator; Provided data is:\n{json.dumps(data,indent=4)}",
                        status=400)
    result = utils.calculate_caloric_needs_per_day(bmr=int(utils.calculate_bmr(weight_in_kg=float(data.get('weight')),
                                                                               height_in_cm=float(data.get('height')),
                                                                               age_in_years=int(data.get('age')),
                                                                               gender=data.get('gender'))),
                                                   activity_level=data.get('activity'))
    return jsonify({'daily_calories': result})

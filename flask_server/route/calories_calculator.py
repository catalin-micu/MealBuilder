import json
from flask import Blueprint, request, Response, jsonify
from flask_server import utils

calories_calculator_blueprint = Blueprint('calories_calculator_blueprint', __name__, url_prefix='/calories-calculator')
REQUIRED_PARAMS_FOR_DAILY_CALORIES = {'weight', 'height', 'age', 'gender', 'activity', 'goal'}
VALID_GOAL_VALUES = {'maintenance', 'lose', 'gain'}


def validate_request_data_for_daily_calories(data: dict) -> bool:
    for param in REQUIRED_PARAMS_FOR_DAILY_CALORIES:
        if param not in list(data.keys()):
            return False
    return True


def modify_daily_calories_based_on_goal(maintenance_calories: int, goal: str) -> int:
    if goal not in VALID_GOAL_VALUES:
        raise ValueError(f"Invalid goal; provided value is '{goal}'")
    if goal == 'maintenance':
        return maintenance_calories
    elif goal == 'lose':
        return maintenance_calories - 250
    elif goal == 'gain':
        return maintenance_calories + 250


@calories_calculator_blueprint.route('/calculate-caloric-needs-per-day', methods=['POST'])
def calculate_daily_calories():
    """
    Request body:
    {
        "weight": 83.5,
        "height": 179,
        "age": 23,
        "gender": "male",
        "activity": "moderate",
        "goal": "gain"
    }
    Possible values:
        gender: [male, female]
        activity: [sedentary, light, moderate, very, extra]
        goal: [maintenance, lose, gain]
    """
    data = request.json
    if not validate_request_data_for_daily_calories(data):
        return Response(f"Invalid params for daily calories calculator; Provided data is:\n{json.dumps(data,indent=4)}",
                        status=400)
    maintenance_calories = utils.calculate_caloric_needs_per_day(bmr=int(utils.calculate_bmr(
        weight_in_kg=float(data.get('weight')),
        height_in_cm=float(data.get('height')),
        age_in_years=int(data.get('age')),
        gender=data.get('gender'))),
            activity_level=data.get('activity'))
    return jsonify({'daily_calories': modify_daily_calories_based_on_goal(maintenance_calories=int(maintenance_calories),
                                                                          goal=data.get('goal'))})

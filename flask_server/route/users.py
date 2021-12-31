from flask import jsonify, Blueprint

users_blueprint = Blueprint('users_blueprint', __name__, url_prefix='/users')


@users_blueprint.route('/testing')
def _test_view():
    return "<h1> SA MOARA BAIETII!!! </h1>"

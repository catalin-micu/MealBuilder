from flask import jsonify, Blueprint
from flask_server.model.sessions import Sessions
from flask_server.model.users import Users

users_blueprint = Blueprint('users_blueprint', __name__, url_prefix='/users')
users = Users()
sessions = Sessions()


@users_blueprint.route('/testing')
def _test_view():
    return "<h1> SA MOARA BAIETII!!! </h1>"


@users_blueprint.route('/login')
def login():
    """
    check params
    if params ok, create session_table entry, allow access
    else deny access
    :return: allow = 200, deny = 403
    """

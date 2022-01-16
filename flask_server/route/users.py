from flask import jsonify, Blueprint, request, Response
from flask_server.model.sessions import Sessions
from flask_server.model.users import Users

users_blueprint = Blueprint('users_blueprint', __name__, url_prefix='/users')
users = Users()
sessions = Sessions()


@users_blueprint.route('/testing')
def _test_view():
    return "<h1> SA MOARA BAIETII!!! </h1>"


@users_blueprint.route('/login', methods=['POST'])
def login():
    """
    check params
    if params ok, create session_table entry, allow access
    else deny access
    request = dict with two keys: email, passwd
    :return: allow = 200, deny = 403
    todo: regex validation for credentials -> rasssvan
    """
    data = request.json
    email = data.get('email')
    passwd = data.get('passwd')

    if users.check_login_credentials(email, passwd):
        # sessions.create_session_from_email(email)
        user_data = users.get_user_data_from_email(email)
        return jsonify(user_data)
    else:
        return Response(f"Invalid credentials! Access denied", status=403)


@users_blueprint.route('/logout', methods=['POST'])
def logout():
    """
     deletes session for logged user
     request body will be { "email": "<value>" }
    """
    email = request.json.get('email')
    user_id = users.get_user_id_from_email(email)
    sessions.delete_session(user_id)

    return Response(f"User with email '{email}' was logged out and corresponding session was deleted", status=200)


@users_blueprint.route('/sign-up', methods=['POST'])
def sign_up():
    """
    creates user table entry
    {
        "email" : "value",
        "passwd" : "value",
        "full_name" : "value",
        "phone_number" : "value"
    }
    """
    user_data = request.json
    users.insert_user(user_data)

    return Response(f"Successfully created user for email '{user_data.get('email')}'", status=200)

from flask import jsonify, Blueprint, request, Response, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from flask_server.model.sessions import Sessions
from flask_server.model.users import Users
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token, jwt_required,
    decode_token, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

users_blueprint = Blueprint('users_blueprint', __name__, url_prefix='/users')
users = Users()
sessions = Sessions()


@users_blueprint.route('/testing')
def _test_view():
    return "<h1> SA MOARA BAIETII!!! </h1>"


@users_blueprint.route('/get-name', methods=['POST'])
@jwt_required
def func():
    email = request.json.get('email')
    if not email:
        return Response("no email in body", status=404)
    return jsonify({'name': users.get_user_data_from_email(email).get('full_name')})


@users_blueprint.route('/get-user', methods=['POST'])
@jwt_required
def get_user():
    email = request.json.get('email')
    if not email:
        return Response("no email in body", status=404)

    current_user = users.get_user_data_from_email_standard_addresses(email)
    return jsonify(current_user)


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

    if not data or not email or not passwd:
        # sessions.create_session_from_email(email)
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = users.get_user_data_from_email(email)

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.get('passwd'), data.get('passwd')):
        # Create the tokens we will be sending back to the user
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        # Set the JWT cookies in the response
        resp = jsonify({'login': True, 'token': access_token})
        # set_access_cookies(resp, access_token)
        # set_refresh_cookies(resp, refresh_token)

        return make_response(resp, 200)
        # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


@users_blueprint.route('/logout', methods=['POST'])
def logout():
    """
     deletes session for logged user
     request body will be { "email": "<value>" }
    """
    email = request.json.get('email')
    user_id = users.get_user_id_from_email(email)
    sessions.delete_session(user_id)
    resp = jsonify({'logout': True})
    # unset_jwt_cookies(resp)
    return resp, 200

    # return Response(f"User with email '{email}' was logged out and corresponding session was deleted", status=200)


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
    user_data['passwd'] = generate_password_hash(request.json.get('passwd'))
    users.insert_user(user_data)

    return Response(f"Successfully created user for email '{user_data.get('email')}'", status=200)


@users_blueprint.route('/decode-token', methods=['POST'])
def decode():
    token = request.json.get('token')

    try:
        # decoding the payload to fetch the stored details
        data = decode_token(token)
        current_user = users.get_user_data_from_email(data.get('identity'))
    except:
        return jsonify({
            'message': 'Token is invalid !!'
        }), 401

    return jsonify({'email': current_user.get('email')})


@users_blueprint.route('/update', methods=['POST'])
def user_update():
    """
        updates user by email
        {
        "email" : "jane.doe@hotmail.com",
        "full_name" : "Jane Doe3",
        "card_nb" : "1234",
        "card_holder_name" : "Jane-Doe",
        "card_expiry" : "07/26",
        "cvv" : 123,
        "phone_number": "0712345678"
    }
        """
    user_data = request.json
    users.update_user(user_data.get('email'), 'email', user_data)

    return Response(f"Successfully updated user for email '{user_data.get('email')}'", status=200)

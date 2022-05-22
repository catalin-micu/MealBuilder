from flask import Flask
from flask_cors import CORS
from flask_server.model.users import Users
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mbdedproject'
# app.config['JWT_TOKEN_LOCATION'] = ['cookies']
#
# # Set the cookie paths, so that you are only sending your access token
# # cookie to the access endpoints, and only sending your refresh token
# # to the refresh endpoint. Technically this is optional, but it is in
# # your best interest to not send additional cookies in the request if
# # they aren't needed.
# app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
# app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'

# Disable CSRF protection for this example. In almost every case,
# this is a bad idea. See examples/csrf_protection_with_cookies.py
# for how safely store JWTs in cookies
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = 'mbded-ba'  # Change this!

jwt = JWTManager(app)

if __name__ == '__main__':

    from flask_server.route import BLUEPRINTS

    # jwt.init_app(app)

    for bp in BLUEPRINTS:
        app.register_blueprint(blueprint=bp)

    CORS(app)

    app.run(debug=True)

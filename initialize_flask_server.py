from flask import Flask
from flask_cors import CORS
from flask_server.model.users import Users
from flask_jwt_extended import JWTManager

app = Flask(__name__)

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

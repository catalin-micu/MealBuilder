from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mbdedproject'

if __name__ == '__main__':

    from flask_server.route import BLUEPRINTS

    for bp in BLUEPRINTS:
        app.register_blueprint(blueprint=bp)

    CORS(app)

    app.run(debug=True)

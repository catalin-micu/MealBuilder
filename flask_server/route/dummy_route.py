"""
created in order to test api routing
"""
from flask import jsonify, Blueprint

dummy_api = Blueprint('dummy_api', __name__)


@dummy_api.route('/')
def index():
    return "<h1>ASHEA TATA</h1>"

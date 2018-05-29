from flask import Blueprint, jsonify

from app.models.user import User


app = Blueprint('user', __name__)


@app.route('/user', methods=['GET'])
def get():
    result = User.get()

    return jsonify(result)

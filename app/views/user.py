from flask import Blueprint, jsonify

from app.models.user import User


app = Blueprint('user', __name__)


@app.route('/user', methods=['GET'])
def get_all():
    result = User.get_all()

    return jsonify(result)


@app.route('/user/<user_id>', methods=['GET'])
def get(user_id):
    result = User.get(user_id)

    return jsonify(result)

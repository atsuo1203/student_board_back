from flask import Blueprint, jsonify, request

from app.models.user import User
from app.views.utils import parse_params


app = Blueprint('user', __name__)


@app.route('/user', methods=['GET'])
def get_all():
    '''すべてのuser情報取得
    Returns:
        list(dict):
            user_id, email, nick_name, profile, twitter_name
    '''
    result = User.get_all()

    return jsonify(result)


@app.route('/user/<user_id>', methods=['GET'])
def get(user_id):
    '''user_idに紐づくuser情報取得
    Returns:
        dict:
            nick_name, profile, twitter_name
    '''
    result = User.get(user_id)

    return jsonify(result)


@app.route('/user/<user_id>', methods=['PUT'])
def put(user_id):
    '''user情報を更新
    引数の内容を変更する（必須ではない）

    Args:
        dict:
            email, nick_name, profile, twitter_name
    Returns:
        dict:
            user_id, email, nick_name, profile, twitter_name
    '''
    params = parse_params(request.form)

    result = User.put(user_id, params)

    return jsonify(result)

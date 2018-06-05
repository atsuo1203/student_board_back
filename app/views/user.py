from flask import Blueprint, jsonify

from app.models.user import User


app = Blueprint('user', __name__)


@app.route('/user', methods=['GET'])
def get_all():
    '''すべてのuser情報取得
    Returns:
        list(dict):
            user_id, email, nick_name, profile, twitter_name
    '''
    result = User.all()

    return jsonify(result)


@app.route('/user/<user_id>', methods=['GET'])
def get(user_id):
    '''user_idに紐づくuser情報取得
    Returns:
        dict:
            user_id, email, nick_name, profile, twitter_name
    '''
    result = User.get(user_id)

    return jsonify(result)

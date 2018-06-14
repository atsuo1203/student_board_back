from flask import Blueprint, jsonify, make_response, request

from app.models.thread import Thread
from app.views.utils import parse_params


app = Blueprint('thread', __name__)


@app.route('/threads/<category_id>', methods=['GET'])
def get_all_by_category_id(category_id):
    '''category_idに紐づけられたthreadリストの取得
    Args:
        category_id:    カテゴリID
    Returns:
        list(dict):
            threads情報(dict)のリスト
    '''
    result = Thread.get_all_by_category_id(category_id)

    return jsonify(result)


@app.route('/thread/<thread_id>', methods=['GET'])
def get(thread_id):
    '''thread_idからthread情報取得
    Args:
        thread_id:  スレッドID
    Returns:
        dict:
            thread: thread情報
            comments: list(dict) comment情報のリスト
    '''
    result = Thread.get(thread_id)

    return jsonify(result)


@app.route('/thread', methods=['POST'])
def post():
    '''threadを作成
    Args:
        title:          スレッドタイトル
        category_id:    カテゴリID
    Returns:
        dict:
            作成されたthread情報
    '''
    params = parse_params(request.form)

    result = Thread.post(params)

    return jsonify(result)


@app.route('/thread', methods=['DELETE'])
def delete():
    '''threadを削除
    同時に，thread_idに紐づくcommentテーブルも削除する
    Args:
        thread_id:  スレッドID
    Returns:
        200:    正常削除
    '''
    params = parse_params(request.form)

    Thread.delete(params)

    return make_response('', 200)

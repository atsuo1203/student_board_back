from flask import Blueprint, jsonify, make_response, request

from app.models.thread import Thread
from app.views.utils import parse_params


app = Blueprint('thread', __name__)


@app.route('/threads', methods=['GET'])
def get_all_by_c_id():
    '''category_idに紐づけられたthreadリストの取得
    Args:
        category_id:    カテゴリID
        sort_id:        ソートID
        paging:         ページング番号
    Returns:
        200:
            list(dict):
                threads情報(dict)のリスト
        400: パラメータ不正

    ページング番号 1の時は1~10，2の時11~20のthreadを取得
    '''
    try:
        params = parse_params(request.form)

        category_id = int(params.get('category_id'))
        sort_id = int(params.get('sort_id'))
        paging = int(params.get('paging'))

        if not category_id or not sort_id or not paging:
            return make_response('', 400)

        result = Thread.get_all_by_c_id(
            category_id,
            sort_id,
            paging
        )

        return jsonify(result)
    except Exception as e:
        return make_response('', 500)


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

    thread_id = params.get('thread_id')

    Thread.delete(thread_id)

    return make_response('', 200)

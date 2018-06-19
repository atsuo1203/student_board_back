from flask import Blueprint, make_response, request

from app.models.comment import Comment
from app.views.utils import parse_params
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('comment', __name__)


@app.route('/comment', methods=['POST'])
@check_webtoken(extra_token=True)
def post_comment(token_data):
    '''comment投稿
    Args:
        name:       名前
        text:       コメントテキスト
        user_id:    ユーザID
        thread_id:  スレッドID
    Returns:
        200:    正常終了
        500:    サーバエラー
    '''
    params = parse_params(request.form)

    try:
        Comment.post(params)

        return make_response('', 201)
    except Exception as e:
        return make_response('Error: Failed post comment', 500)

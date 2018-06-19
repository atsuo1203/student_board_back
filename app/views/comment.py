from flask import Blueprint, make_response, request

from app.models.comment import Comment
from app.models.user import User
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('comment', __name__)


@app.route('/comment', methods=['POST'])
@check_webtoken(extra_token=True)
def post_comment(token_data):
    '''comment投稿
    Args:
        text:       コメントテキスト
        thread_id:  スレッドID
    Returns:
        200:    正常終了
        500:    サーバエラー
    '''
    params = request.json

    user_id = token_data.get('user_id')
    user = User.get(user_id=user_id)

    params.update({
        'user_id': user_id,
        'name': user.get('nick_name')
    })

    try:
        Comment.post(params)

        return make_response('', 201)
    except Exception as e:
        return make_response('', 500)

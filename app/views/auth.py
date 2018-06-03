from datetime import datetime
from flask import Blueprint, jsonify, make_response, request

from app.config import EXPIRE_TIME, FROM_ADDRESS, FROM_ADDRESS_PASS
from app.models.provisional_user import ProvisionalUser
from app.models.user import User
from app.views.utils import parse_params, send_confirm_mail


app = Blueprint('auth', __name__)


@app.route('/auth/prov_user', methods=['POST'])
def register_prov_user():
    '''ユーザの仮登録を行う
    Args:
        email:  学番メール
    Returns:
        200:    正常に登録が行われた
        400:    不正なメールアドレス
        500:    サーバエラー
    '''
    try:
        params = parse_params(request.form)

        email = params['email']

        # 仮登録を行う
        # トークンを返却
        # TODO 仮登録を連続で登録できないようにinterva_timeを設定する
        token = ProvisionalUser.post(email)

        # 確認メール送信
        send_confirm_mail(
            from_addr=FROM_ADDRESS,
            from_addr_pass=FROM_ADDRESS_PASS,
            to_addr=email,
            token=token
        )

        return make_response('', 200)
    except Exception as e:
        print(e)
        return make_response('', 500)


@app.route('/auth/register', methods=['POST'])
def register():
    '''ユーザの本登録を行う
    Args:
        email:  学番メール
        token:  仮登録のトークン
        password:   パスワード
    Returns:
        200:    正常登録
        400:    仮登録ユーザが存在しない，トークンの有効期限切れ，トークンの不一致
            error_message:  エラーメッセージ（必要なエラーのみ）
        500:    サーバエラー
    '''
    try:
        params = parse_params(request.form)

        email = params['email']
        token = params['token']
        password = params['password']

        # ユーザがすでに本登録されているか
        if User.is_exist(email):
            # ユーザが登録されている場合，400を返す
            result = {
                'error_message': 'このメールアドレスは既に使われています'
            }
            return make_response(jsonify(result), 400)

        # 仮登録ユーザを学番メールから検索し，最新の仮登録ユーザを取得
        prov_user = ProvisionalUser.get(email)

        # 仮登録ユーザが存在しない場合，400を返却
        if not prov_user:
            result = {
                'error_message': '仮登録を行なってください'
            }
            return make_response(jsonify(result), 400)

        # 仮登録作成時間と現在時間の差分を取得
        delta = datetime.now() - prov_user['create_at']

        # 有効時間切れの場合，400を返却
        if delta.total_seconds() > EXPIRE_TIME:
            result = {
                'error_message': '有効期限切れです'
            }
            return make_response(jsonify(result), 400)

        # トークンが不一致の場合，400を返却
        if token != prov_user['token']:
            result = {
                'error_message': '有効期限切れです'
            }
            return make_response(jsonify(result), 400)

        # ユーザ本登録
        result = User.post(
            email=email,
            password=password
        )

        return jsonify(result)
    except:
        return make_response('', 500)

import secrets
from datetime import datetime

from app.database import db
from app.models import row_to_dict, session_scope


class ProvisionalUser(db.Model):
    __tablename__ = 'provisional_user'

    provisional_user_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    email = db.Column(db.String(length=256), nullable=False)
    token = db.Column(db.String(length=256), nullable=False)
    create_at = db.Column(db.DateTime(), nullable=False)

    @classmethod
    def get(cls, email):
        '''仮登録ユーザの最新のカラムを取得
        Args:
            email:  学番メール
        Returns:
            dict:
                ProvisionalUser:    仮登録ユーザ情報
        '''
        with session_scope() as session:
            # prov_user = session.
            rows = session.query(
                cls
            ).filter(
                cls.email == email
            ).order_by(
                cls.provisional_user_id.desc()
            ).first()

            return row_to_dict(rows)

    @classmethod
    def post(cls, email):
        '''ユーザ仮登録
        Args:
            email:  学番メール
        Returns:
            token:  トークン
        '''
        with session_scope() as session:
            # 推測しにくい一時URLトークン生成
            token = secrets.token_urlsafe()

            data = cls(
                email=email,
                token=token,
                create_at=datetime.now()
            )
            session.add(data)

            return token

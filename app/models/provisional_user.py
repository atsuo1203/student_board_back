import secrets
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from app.models import Base, row_to_dict, session_scope


class ProvisionalUser(Base):
    __tablename__ = 'provisional_user'

    provisional_user_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    email = Column(String(length=256), nullable=False)
    login_token = Column(String(length=256), nullable=False)
    create_at = Column(DateTime, nullable=False)

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
            login_token:  ログイントークン
        '''
        with session_scope() as session:
            # 推測しにくい一時URLトークン生成
            login_token = secrets.token_urlsafe()

            data = cls(
                email=email,
                login_token=login_token,
                create_at=datetime.now()
            )
            session.add(data)

            return login_token

from app.database import db
from app.models import row_to_dict, session_scope


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    email = db.Column(db.String(length=256), nullable=False)
    password = db.Column(db.String(length=256), nullable=False)
    nick_name = db.Column(db.String(length=256), nullable=True)
    profile = db.Column(db.String(length=256), nullable=True)
    twitter_name = db.Column(db.String(length=256), nullable=True)

    @classmethod
    def get(cls, user_id):
        '''user_idに紐づくuser情報取得
        Args:
            user_id: ユーザID
        Returns:
            dict: user情報
        '''
        with session_scope() as session:
            rows = session.query(
                cls.user_id,
                cls.email,
                cls.nick_name,
                cls.profile,
                cls.twitter_name
            ).filter(
                cls.user_id == user_id
            ).first()

            return rows._asdict()

    @classmethod
    def get_all(cls):
        '''すべてのuser情報取得
        '''
        with session_scope() as session:
            rows = session.query(
                cls.user_id,
                cls.email,
                cls.nick_name,
                cls.profile,
                cls.twitter_name
            ).all()

            result = [row._asdict() for row in rows]

            return result

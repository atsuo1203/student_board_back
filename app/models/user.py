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
    def all(cls):
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

    @classmethod
    def login(cls, email, password):
        '''emailとpasswordが一致するuser情報を取得
        Args:
            email:      学番メール
            password:   パスワード
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
                cls.email == email,
                cls.password == password
            ).order_by(
                cls.user_id.desc()
            ).first()

            if not rows:
                return None

            return rows._asdict()

    @classmethod
    def is_exist(cls, email):
        '''同じ学番メールのユーザが存在するかどうかをboolで返却
        Args:
            email:      学番メール
        Returns:
            bool:
        '''
        with session_scope() as session:
            count = session.query(
                cls
            ).filter(
                cls.email == email
            ).count()

            if count > 0:
                return True
            else:
                return False

    @classmethod
    def post(cls, email, password):
        '''user登録
        Args:
            email:      学番メール
            password:   パスワード
        Returns:
            dict: user情報
                user_id:    ユーザID
                email:      学番メール
        '''
        with session_scope() as session:
            data = cls(
                email=email,
                password=password
            )
            session.add(data)
            session.flush()

            result = {
                'user_id': data.user_id,
                'email': data.email,
            }

            return result

    @classmethod
    def put(cls, user_id, params):
        with session_scope() as session:
            data = cls(
                user_id=user_id,
                **params
            )

            # mergeして1回commit
            session.merge(data)
            session.commit()

            # commit後の更新されたuser情報取得
            user = cls.get(user_id)

            return user

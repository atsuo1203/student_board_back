from .category import Category
from app.database import db
from app.models import row_to_dict, session_scope


class Thread(db.Model):
    __tablename__ = 'thread'

    thread_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    title = db.Column(db.String(length=256), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    speed = db.Column(db.Integer, nullable=True)
    comment_count = db.Column(db.Integer, nullable=True)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey(Category.category_id),
        nullable=False,
    )

    @classmethod
    def get_threads(cls, category_id):
        '''category_idに紐づけられたthreadリストの取得
        Args:
            category_id: カテゴリID
        Returns:
            list(dict): threads情報(dict)のリスト
        '''
        with session_scope() as session:
            rows = session.query(
                cls.thread_id,
                cls.title,
                cls.date
            ).join(
                Category, Thread.category_id == Category.category_id
            ).filter(
                Category.category_id == category_id
            ).all()

            result = [row._asdict() for row in rows]

            return result

    @classmethod
    def get(cls, thread_id):
        '''thread_idからthread情報取得
        Args:
            thread_id: スレッドID
        Returns:
            dict: thread情報
        '''
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.thread_id == thread_id
            ).first()

            return row_to_dict(rows)

    @classmethod
    def post(cls, params):
        '''threadを作成
        Args:
            params (dict):
                title: スレッドタイトル
                category_id: カテゴリID
        Returns:
            dict: 作成されたthread情報
        '''
        with session_scope() as session:
            data = cls(
                title=params['title'],
                category_id=params['category_id']
            )
            session.add(data)
            session.flush()

            from .comment import create_db

            # コメントテーブルを動的に作成する
            create_db(data.thread_id)

            return row_to_dict(data)

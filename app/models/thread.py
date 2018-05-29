from app.database import db
from app.models import row_to_dict, session_scope

from .category import Category


class Thread(db.Model):
    __tablename__ = 'thread'

    thread_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name = db.Column(db.String(length=256), nullable=False)
    date = db.Column(db.Date(), nullable=False)
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
                cls.name,
                cls.date
            ).join(
                Category, Thread.category_id == Category.category_id
            ).filter(
                Category.category_id == category_id
            ).all()

            result = [row._asdict() for row in rows]

            return result

    @classmethod
    def post(cls, params):
        '''threadを作成
        Args:
            params (dict):
                name: スレッドタイトル
                category_id: カテゴリID
        Returns:
            dict: 作成されたthread情報
        '''
        with session_scope() as session:
            result = session.query(cls).all()
            print(result)

            data = cls(
                name=params['name'],
                category_id=params['category_id']
            )
            session.add(data)
            session.flush()

            result = row_to_dict(data)

        return result

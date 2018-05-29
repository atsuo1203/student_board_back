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

    def get_threads():
        rows = db.session.query(
            Thread.thread_id,
            Thread.name,
            Thread.date,
            Category.category_id,
            Category.name
        ).join(
            Category, Thread.thread_id == Category.category_id
        ).all()


        result = [row._asdict() for row in rows]
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

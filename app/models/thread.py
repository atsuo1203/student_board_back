from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from .category import Category
from app.config import Config
from app.database import db
from app.models import row_to_dict, session_scope


engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    echo=False,
    encoding='utf-8'
)
base = declarative_base(engine)


class Thread(db.Model):
    __tablename__ = 'thread'

    thread_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    title = db.Column(db.String(length=256), nullable=False)
    create_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    update_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    speed = db.Column(db.Integer, nullable=True, default=0)
    comment_count = db.Column(db.Integer, nullable=True, default=0)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey(Category.category_id),
        nullable=False,
    )

    @classmethod
    def all(cls, category_id):
        with session_scope() as session:
            rows = session.query(
                cls
            ).join(
                Category, Thread.category_id == Category.category_id
            ).filter(
                Category.category_id == category_id
            ).all()

            result = [row_to_dict(row) for row in rows]

            return result

    @classmethod
    def get(cls, thread_id):
        with session_scope() as session:
            # thread情報取得
            thread_rows = session.query(cls).filter(
                cls.thread_id == thread_id
            ).first()

            # thread_idに紐づくcomment情報取得
            # テーブル名を指定する
            management_dic = {
                '__tablename__': 'comment' + str(thread_id),
                '__table_args__': {'autoload': True}}
            management_object = type('management_object', (base,), management_dic)
            comment_rows = session.query(management_object).all()
            comment_list = [row_to_dict(row) for row in comment_rows]

            result = {
                'thread': row_to_dict(thread_rows),
                'comments': comment_list
            }

            return result

    @classmethod
    def post(cls, params):
        with session_scope() as session:
            data = cls(
                title=params['title'],
                category_id=int(params['category_id'])
            )
            session.add(data)
            session.flush()

            from .comment import create_db

            # コメントテーブルを動的に作成する
            create_db(data.thread_id)

            return row_to_dict(data)

    @classmethod
    def delete(cls, params):
        with session_scope() as session:
            rows = session.query(cls).filter_by(thread_id=params['thread_id'])
            for row in rows:
                session.delete(row)

    @classmethod
    def add_comment_count(cls, session, thread_id):
        data = cls(
            thread_id=thread_id,
            comment_count=(cls.comment_count + 1)
        )

        session.merge(data)

        return

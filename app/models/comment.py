from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from .thread import Thread
from .user import User
from app.config import Config
from app.database import db
from app.models import session_scope


engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    echo=False,
    encoding='utf-8'
)
base = declarative_base(engine)


class Comment(db.Model):
    __tablename__ = 'comment'

    comment_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name = db.Column(db.String(length=256), nullable=False)
    text = db.Column(db.String(length=256), nullable=False)
    create_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    thread_id = db.Column(
        db.Integer,
        db.ForeignKey(Thread.thread_id),
        nullable=False,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(User.user_id),
        nullable=False,
    )


    @classmethod
    def post(cls, thread_id, params):
        comment_table = cls.__table__
        comment_table.name = 'comment' + str(thread_id)

        with session_scope() as session:
            # thread_idに紐づくcommentテーブルにcomment投稿
            # テーブル名を指定する
            comment_table_dic = {
                '__tablename__': 'comment' + str(thread_id),
                '__table_args__': {'autoload': True}}
            comment_table = type('comment_table', (base,), comment_table_dic)

            data = comment_table(
                name=params['name'],
                text=params['text'],
                create_at=datetime.now(),
                thread_id=thread_id,
                user_id=params['user_id']
            )
            session.add(data)

            Thread.add_comment_count(session, thread_id)

            return

    @classmethod
    def delete(cls, thread_id):
        comment_table = cls.__table__
        comment_table.name = 'comment' + str(thread_id)
        comment_table.drop(engine)

        return


def create_db(thread_id):
    '''コメントテーブルを動的に作成する
    テーブル名は，comment + thread_id
    '''
    comment_table = Comment.__table__
    comment_table.name = 'comment' + str(thread_id)
    comment_table.create(engine)

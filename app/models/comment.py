from datetime import datetime
from sqlalchemy import create_engine

from .thread import Thread
from .user import User
from app.config import Config
from app.database import db


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
    date = db.Column(db.DateTime(), nullable=False, default=datetime.now())
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


def create_db(pid):
def create_db(thread_id):
    '''コメントテーブルを動的に作成する
    テーブル名は，comment + thread_id
    '''
    engine = create_engine(
        Config.SQLALCHEMY_DATABASE_URI,
    )

    comment_table = Comment.__table__
    comment_table.name = 'comment' + str(thread_id)
    comment_table.create(engine)

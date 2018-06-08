from datetime import datetime

from sqlalchemy import (
    Column, DateTime, ForeignKey, Integer, String, create_engine
)
from sqlalchemy.ext.declarative import declarative_base

from app.config import create_dburl
from app.models import session_scope
from app.models.thread import Thread
from app.models.user import User


# commentテーブルだけ独自のBaseを継承
Base = declarative_base()


class Comment(Base):
    __tablename__ = 'comment'

    comment_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name = Column(String(length=256), nullable=False)
    text = Column(String(length=256), nullable=False)
    create_at = Column(DateTime, nullable=False, default=datetime.now())
    thread_id = Column(
        Integer,
        ForeignKey(Thread.thread_id),
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey(User.user_id),
        nullable=False,
    )


    @classmethod
    def post(cls, thread_id, params):
        comment_table = cls.__table__
        comment_table.name = 'comment' + str(thread_id)

        with session_scope() as session:
            # thread_idに紐づくcommentテーブルにcomment投稿
            # テーブル名を指定する
            dburl = create_dburl()
            engine = create_engine(dburl)
            base = declarative_base(engine)

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
        dburl = create_dburl()
        engine = create_engine(dburl)

        comment_table = cls.__table__
        comment_table.name = 'comment' + str(thread_id)
        comment_table.drop(engine)

        return


def create_db(thread_id):
    '''コメントテーブルを動的に作成する
    テーブル名は，comment + thread_id
    '''
    dburl = create_dburl()
    engine = create_engine(dburl)

    comment_table = Comment.__table__
    comment_table.name = 'comment' + str(thread_id)
    comment_table.create(engine)

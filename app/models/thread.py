from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.models import Base, row_to_dict, session_scope
from app.models.category import Category


class Thread(Base):
    __tablename__ = 'thread'

    thread_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    title = Column(String(length=256), nullable=False)
    create_at = Column(DateTime, nullable=False, default=datetime.now())
    update_at = Column(DateTime, nullable=False, default=datetime.now())
    speed = Column(Integer, nullable=True, default=0)
    comment_count = Column(Integer, nullable=True, default=0)
    category_id = Column(
        Integer,
        ForeignKey(Category.category_id),
        nullable=False,
    )

    @classmethod
    def get(cls, thread_id):
        '''threadとthread_idに紐づくcomment取得
        '''
        from app.models.comment import Comment

        with session_scope() as session:
            # thread取得
            t_rows = session.query(cls).filter(
                cls.thread_id == thread_id
            ).first()

            # thread_idに紐づくcommentリスト取得
            comments = Comment.get_all_by_t_id(thread_id)

            result = {
                'thread': row_to_dict(t_rows),
                'comments': comments,
            }

            return result

    @classmethod
    def get_all(cls):
        '''すべてのthread情報取得
        '''
        with session_scope() as session:
            rows = session.query(cls).all()

            result = [row_to_dict(row) for row in rows]

            return result

    @classmethod
    def get_all_by_c_id(cls, category_id):
        '''category_idに紐づくthreadリスト取得
        '''
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
    def post(cls, params):
        with session_scope() as session:
            data = cls(**params)
            session.add(data)
            session.flush()

            return row_to_dict(data)

    @classmethod
    def delete(cls, params):
        with session_scope() as session:
            thread_id = params['thread_id']

            row = session.query(cls).filter_by(thread_id=thread_id).first()

            session.delete(row)

            # *** TODO thread_idに紐づくcomment削除

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.models import Base, session_scope, row_to_dict
from app.models.thread import Thread
from app.models.user import User


class Comment(Base):
    __tablename__ = 'comment'

    comment_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    thread_id = Column(
        Integer,
        ForeignKey(Thread.thread_id),
        nullable=False,
        index=True
    )
    name = Column(String(length=256), nullable=False)
    text = Column(String(length=256), nullable=False)
    create_at = Column(
        DateTime, nullable=False, default=datetime.now()
    )
    user_id = Column(
        Integer,
        ForeignKey(User.user_id),
        nullable=False,
    )

    @classmethod
    def get_all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            result = [row_to_dict(row) for row in rows]

            return result

    @classmethod
    def get_all_by_t_id(cls, thread_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.thread_id == thread_id
            ).all()

            result = [row_to_dict(row) for row in rows]

            return result

    @classmethod
    def post(cls, params):
        with session_scope() as session:
            data = cls(**params)
            session.add(data)

            # thread_idに紐づくthreadのcomment_count加算

            return

    # def add_comment_count(cls, session, thread_id):
    #     data = cls(
    #         thread_id=thread_id,
    #         comment_count=(cls.comment_count + 1)
    #     )

    #     session.merge(data)

    #     return

from app.models import Base, row_to_dict, session_scope
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


class Category(Base):
    __tablename__ = 'category'

    category_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name = Column(String(length=256), nullable=False)

    def get():
        with session_scope() as session:
            rows = session.query(Category).all()

            result = [row_to_dict(row) for row in rows]

            return result

from app.database import db
from app.models import row_to_dict, session_scope


class University(db.Model):
    __tablename__ = 'university'

    university_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name = db.Column(db.String(length=256), nullable=False)
    domain = db.Column(db.String(length=256), nullable=False)

    @classmethod
    def get_all(cls):
        '''すべてのuniversity情報取得
        Returns:
            list(dict): university情報(dict)のリスト
        '''
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]


    @classmethod
    def get(cls, university_id):
        '''university_idに紐づくuniversity情報取得
        Args:
            university_id: 大学ID
        Returns:
            list(dict): university情報(dict)のリスト
        '''
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.university_id == university_id
            ).first()

            return row_to_dict(rows)
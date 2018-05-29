from app.database import db
from app.models import row_to_dict


class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name = db.Column(db.String(length=256), nullable=False)

    def get():
        rows = db.session.query(Category).all()

        result = [row_to_dict(row) for row in rows]

        return result


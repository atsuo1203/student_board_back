from app.database import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(length=256), nullable=False)
    password = db.Column(db.String(length=256), nullable=False)

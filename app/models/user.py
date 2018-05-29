from app.database import db


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    email = db.Column(db.String(length=256), nullable=False)
    password = db.Column(db.String(length=256), nullable=False)
    nick_name = db.Column(db.String(length=256), nullable=True)
    profile = db.Column(db.String(length=256), nullable=True)
    twitter_name = db.Column(db.String(length=256), nullable=True)

    def get():
        rows = db.session.query(
            User.user_id,
            User.email,
            User.nick_name,
            User.profile,
            User.twitter_name
        ).all()

        result = [row._asdict() for row in rows]

        return result

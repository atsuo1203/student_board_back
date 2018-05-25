from flask import Blueprint

from app.database import db
from app.models.user import User


app = Blueprint('user', __name__)


@app.route('/user')
def index():
    users = db.session.query(User).all()
    print("users:", users)

    return 'get user'

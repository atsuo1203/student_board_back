from flask import Blueprint

app = Blueprint('thread', __name__)


@app.route('/thread')
def index():
    return 'get thread'

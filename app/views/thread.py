from flask import Blueprint, jsonify

from app.models.thread import Thread


app = Blueprint('thread', __name__)


@app.route('/threads', methods=['GET'])
def get_threads():
    result = Thread.get_threads()

    return jsonify(result)

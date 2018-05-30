from flask import Blueprint, jsonify, make_response, request

from app.models.thread import Thread
from app.views.utils import parse_params


app = Blueprint('thread', __name__)


@app.route('/threads/<category_id>', methods=['GET'])
def get_threads(category_id):
    result = Thread.get_threads(category_id)

    return jsonify(result)


@app.route('/thread/<thread_id>', methods=['GET'])
def get(thread_id):
    result = Thread.get(thread_id)

    return jsonify(result)

@app.route('/thread', methods=['POST'])
def post():
    params = parse_params(request.form)

    result = Thread.post(params)

    return jsonify(result)

@app.route('/thread', methods=['DELETE'])
def delete():
    params = parse_params(request.form)

    Thread.delete(params)

    return make_response('', 200)

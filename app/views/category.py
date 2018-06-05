from flask import Blueprint, jsonify

from app.models.category import Category


app = Blueprint('category', __name__)


@app.route('/category', methods=['GET'])
def get():
    '''すべてのcategory取得
    Returns:
        list(dict):
            category情報のリスト
    '''
    result = Category.get()

    return jsonify(result)

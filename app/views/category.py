from flask import Blueprint, jsonify

from app.models.category import Category
from app.views.utils.check_webtoken import check_webtoken


app = Blueprint('category', __name__)


@app.route('/category', methods=['GET'])
@check_webtoken
def get():
    '''すべてのcategory取得
    Returns:
        list(dict):
            category情報のリスト
    '''
    result = Category.get()

    return jsonify(result)

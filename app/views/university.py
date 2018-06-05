from flask import Blueprint, jsonify

from app.models.university import University


app = Blueprint('university', __name__)


@app.route('/university', methods=['GET'])
def get_all():
    '''すべてのuniversity情報取得
    Returns:
        list(dict):
            university情報(dict)のリスト
    '''
    result = University.all()

    return jsonify(result)


@app.route('/university/<university_id>', methods=['GET'])
def get(university_id):
    '''university_idに紐づくuniversity情報取得
    Args:
        university_id:  大学ID
    Returns:
        list(dict):
            university情報(dict)のリスト
    '''
    result = University.get(university_id)

    return jsonify(result)

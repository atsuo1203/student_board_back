from flask import Blueprint, jsonify

from app.models.university import University


app = Blueprint('university', __name__)


@app.route('/university', methods=['GET'])
def get_all():
    result = University.get_all()

    return jsonify(result)


@app.route('/university/<university_id>', methods=['GET'])
def get(university_id):
    result = University.get(university_id)

    return jsonify(result)

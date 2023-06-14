from flask import Flask, request, jsonify, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from os import access
import validators
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, \
    HTTP_409_CONFLICT

users = {}  # Dictionary to store user credentials

numString = Blueprint("numString", __name__, url_prefix="/api/v1/numString")


@numString.route('/sum', methods=['POST'])
def sum_numbers():
    try:
        data = request.get_json()
        if 'numbers' not in data:
            return jsonify({'message': 'Missing \'numbers\' field in the request body.'}), HTTP_400_BAD_REQUEST

        numbers = data['numbers']
        if not isinstance(numbers, list):
            return jsonify({'message': 'Invalid input format. Expected a list of numbers.'}), HTTP_400_BAD_REQUEST

            # Validate that each element in the list is a number
        for num in numbers:
            if not isinstance(num, (int, float)):
                return jsonify({
                                   'message': 'Invalid input format. All elements in the list must be numbers.'}), HTTP_400_BAD_REQUEST

        result = sum(numbers)
        return jsonify({'result': result})
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), HTTP_400_BAD_REQUEST


@numString.route('/concatenate', methods=['POST'])
def concatenate_strings():
    try:
        data = request.get_json()

        if 'strings' not in data:

            return jsonify({'message': 'Missing \'strings\' field in the request body.'}), HTTP_400_BAD_REQUEST

        strings = data['strings']

        for string in strings:
            if not isinstance(string, str) and len(strings):
                return jsonify({'message': 'Invalid input format. Expected two strings.'}), HTTP_400_BAD_REQUEST

        result = "".join(strings)
        return jsonify({'result': result})

    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), HTTP_400_BAD_REQUEST

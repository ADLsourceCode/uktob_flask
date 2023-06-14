from flask import Flask, request, jsonify, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from os import access
import validators
from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, \
    HTTP_409_CONFLICT

users = {}  # Dictionary to store user credentials

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.route('/register', methods=['POST'])
def register():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        if len(password) < 6:
            return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

        if len(username) < 3:
            return jsonify({'error': "Username is too short"}), HTTP_400_BAD_REQUEST

        if not validators.email(username):
            return jsonify({'error': "Username is not valid"}), HTTP_400_BAD_REQUEST

        if username in users:
            return jsonify({'error': "Username is taken"}), HTTP_409_CONFLICT

        pwd_hash = generate_password_hash(password)
        users[username] = pwd_hash
        return jsonify({'message': 'Registration successful!'})

    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), HTTP_400_BAD_REQUEST


@auth.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        if username and password:
            if username in users:
                is_pass_correct = check_password_hash(users[username], password)
                if is_pass_correct:
                    return jsonify({'message': 'Access granted!'})
                else:
                    return jsonify({'message': 'Access denied!'}), HTTP_401_UNAUTHORIZED
            else:
                return jsonify({'message': 'Access denied!'}), HTTP_401_UNAUTHORIZED

        else:
            return jsonify({'message': 'Missing username or password!'}), HTTP_400_BAD_REQUEST

    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), HTTP_400_BAD_REQUEST

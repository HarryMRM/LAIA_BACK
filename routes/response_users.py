# routes/response_users.py
from flask import Blueprint, request, jsonify
from services.users_admin import create_user, validate_user, update_user, delete_user
response_users_route = Blueprint('response_users', __name__)

@response_users_route.route('/api/response_users', methods=['POST'])
def create_a_user():
    try:
        data = request.get_json()

        if ("user" not in data) or ("password" not in data):
            return jsonify({"error": "Se necesita un usuario (user) y contraseña (password)"}), 400

        created = create_user(data)
        return jsonify(created), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@response_users_route.route('/api/response_users', methods=['GET'])
def validate_a_user():
    try:
        data = request.get_json()

        if ("user" not in data) or ("password" not in data):
            return jsonify({"error": "Se necesita un usuario (user) y contraseña (password)"}), 400
        
        validated = validate_user(data)
        return jsonify(validated), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@response_users_route.route('/api/response_users', methods=['PUT'])
def update_a_user():
    try:
        data = request.get_json()

        if ("user" not in data) or ("password" not in data):
            return jsonify({"error": "Se necesita un usuario (user) y contraseña (password)"}), 400
        
        if ("new_user" not in data) and ("new_password" not in data):
            return jsonify({"error": "Se necesita un nuevo usuario (new_user) o una nueva contraseña (new_password)"}), 400
        
        if ("new_password" in data) and ("code" not in data):
            return jsonify({"error": "Se necesita un código de validación para cambiar la contraseña"}), 400

        updated = update_user(data)
        return jsonify(updated), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@response_users_route.route('/api/response_users', methods=['DELETE'])
def delete_a_user():
    try:
        data = request.get_json()

        if ("user" not in data) or ("password" not in data):
            return jsonify({"error": "Se necesita un usuario (user) y contraseña (password)"}), 400
        
        deleted = delete_user(data)
        return jsonify(deleted), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

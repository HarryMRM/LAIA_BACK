# routes/response_users.py
from flask import Blueprint, request, jsonify
# from services.users_admin import 
response_users = Blueprint('response_users', __name__)

@response_users.route('/api/response_users', methods=['POST'])
def create_user():
    data = request.json
    # Lógica para crear un usuario (puedes reemplazar esto con llamada a un controlador)
    return jsonify({"message": "Usuario creado", "data": data}), 201


@response_users.route('/api/response_users/user_id/<string:user_id>', methods=['GET'])
def get_user(user_id):
    # Lógica para obtener un usuario por ID (puedes agregar acceso a DB)
    return jsonify({"message": f"Obteniendo usuario con ID {user_id}"})


@response_users.route('/api/response_users/user_id/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    # Lógica para actualizar un usuario
    return jsonify({"message": f"Usuario con ID {user_id} actualizado", "data": data})


@response_users.route('/api/response_users/user_id/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Lógica para eliminar un usuario
    return jsonify({"message": f"Usuario con ID {user_id} eliminado"})

# routes/users_admin.py
from flask import Blueprint, request, jsonify

# Creación del blueprint para rutas de usuario
users_admin = Blueprint('users_admin', __name__)

@users_admin.route('/api/users_admin', methods=['POST'])
def create_user():
    data = request.json
    # Lógica para crear un usuario (puedes reemplazar esto con llamada a un controlador)
    return jsonify({"message": "Usuario creado", "data": data}), 201


@users_admin.route('/api/users_admin/<str:user_id>', methods=['GET'])
def get_user(user_id):
    # Lógica para obtener un usuario por ID (puedes agregar acceso a DB)
    return jsonify({"message": f"Obteniendo usuario con ID {user_id}"})


@users_admin.route('/api/users_admin/<str:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    # Lógica para actualizar un usuario
    return jsonify({"message": f"Usuario con ID {user_id} actualizado", "data": data})


@users_admin.route('/api/users_admin/<str:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Lógica para eliminar un usuario
    return jsonify({"message": f"Usuario con ID {user_id} eliminado"})

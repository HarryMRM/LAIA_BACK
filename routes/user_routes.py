# routes/user_routes.py
from flask import Blueprint, request, jsonify

# Creación del blueprint para rutas de usuario
user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/', methods=['POST'])
def create_user():
    data = request.json
    # Lógica para crear un usuario (puedes reemplazar esto con llamada a un controlador)
    return jsonify({"message": "Usuario creado", "data": data}), 201

@user_routes.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Lógica para obtener un usuario por ID (puedes agregar acceso a DB)
    return jsonify({"message": f"Obteniendo usuario con ID {user_id}"})

@user_routes.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    # Lógica para actualizar un usuario
    return jsonify({"message": f"Usuario con ID {user_id} actualizado", "data": data})

@user_routes.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Lógica para eliminar un usuario
    return jsonify({"message": f"Usuario con ID {user_id} eliminado"})

# routes/response_users.py
from flask import Blueprint, request, jsonify
from services.users_admin import (
    create_user,
    validate_user,
    update_user,
    delete_user,
    get_user_info,
)
from services.token_admin import (
    get_access_token,
    get_refresh_token,
    get_new_access_token,
    get_token_from_headers,
)
from utils.authenticate import authenticate

response_users_route = Blueprint("response_users", __name__)


@response_users_route.route("/api/response_users/new", methods=["POST"])
def create_a_user():
    try:
        data = request.get_json()

        if ("user" not in data) or ("password" not in data):
            return (
                jsonify(
                    {"error": "Se necesita un usuario (user) y contraseña (password)"}
                ),
                400,
            )

        created = create_user(data)

        if "error" in created:
            return jsonify(created), 400
        else:
            return jsonify(created), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@response_users_route.route("/api/response_users/validate", methods=["POST"])
def validate_a_user():
    try:
        data = request.get_json()

        if ("user" not in data) or ("password" not in data):
            return (
                jsonify(
                    {"error": "Se necesita un usuario (user) y contraseña (password)"}
                ),
                400,
            )

        validated = validate_user(data)
        print(validated)

        if "error" in validated:
            return jsonify(validated), 400
        else:
            user = {"uid": validated.get("_id"), "user": validated.get("user")}
            access_token = get_access_token(user)
            refresh_token = get_refresh_token(user)
            return (
                jsonify(
                    {
                        "user": user,
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    }
                ),
                200,
            )

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@response_users_route.route("/api/response_users/refresh-token", methods=["POST"])
def get_a_new_access_token():
    try:
        headers = request.headers
        refresh_token = get_token_from_headers(headers)

        if refresh_token:
            new_access_token = get_new_access_token(refresh_token)
            if new_access_token:
                return (
                    jsonify({"new_access_token": new_access_token}),
                    200,
                )
            else:
                return jsonify(new_access_token), 401
        else:
            return (
                jsonify({"error": "No autorizado"}),
                401,
            )

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@response_users_route.route("/api/response_users/user", methods=["GET"])
def get_the_user_info():
    try:
        user = authenticate(request)
        if user:
            if "error" not in user:
                return (
                    jsonify(user),
                    200,
                )
            else:
                print(f"Error: {user}")
                return jsonify(user), 500
        else:
            return (
                jsonify({"error": "No se ha proporcionado un token válido"}),
                401,
            )

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@response_users_route.route("/api/response_users", methods=["PUT"])
def update_a_user():
    try:
        data = request.get_json()

        if ("user" not in data) or ("password" not in data):
            return (
                jsonify(
                    {"error": "Se necesita un usuario (user) y contraseña (password)"}
                ),
                400,
            )

        if ("new_user" not in data) and ("new_password" not in data):
            return (
                jsonify(
                    {
                        "error": "Se necesita un nuevo usuario (new_user) o una nueva contraseña (new_password)"
                    }
                ),
                400,
            )

        if ("new_password" in data) and ("code" not in data):
            return (
                jsonify(
                    {
                        "error": "Se necesita un código de validación para cambiar la contraseña"
                    }
                ),
                400,
            )

        updated = update_user(data)

        if "error" in updated:
            return jsonify(updated), 400
        else:
            return jsonify(updated), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@response_users_route.route("/api/response_users", methods=["DELETE"])
def delete_a_user():
    try:
        data = request.get_json()

        if ("user" not in data) or ("password" not in data):
            return (
                jsonify(
                    {"error": "Se necesita un usuario (user) y contraseña (password)"}
                ),
                400,
            )

        deleted = delete_user(data)

        if "error" in deleted:
            return jsonify(deleted), 400
        else:
            return jsonify(deleted), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

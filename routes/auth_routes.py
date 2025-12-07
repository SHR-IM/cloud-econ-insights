from flask import Blueprint, request, jsonify
from auth import create_user, login

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = create_user(email, password)
    return jsonify(user), 201


@auth_bp.route("/login", methods=["POST"])
def login_route():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    api_key = login(email, password)

    if not api_key:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"api_key": api_key})

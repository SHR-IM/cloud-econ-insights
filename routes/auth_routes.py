"""Registration and login routes."""
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from auth import create_user, login
from models import db

auth_bp = Blueprint("auth", __name__)


def credentials_from_request():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, None
    return data.get("email"), data.get("password")


@auth_bp.route("/register", methods=["POST"])
def register():
    email, password = credentials_from_request()
    if (
        not isinstance(email, str)
        or not isinstance(password, str)
        or "@" not in email
        or " " in email
        or len(email) > 120
        or len(password) < 8
    ):
        return jsonify({"error": "Valid email and password of at least 8 characters required"}), 400

    try:
        user = create_user(email.strip().lower(), password)
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email is already registered"}), 409

    return jsonify(user), 201


@auth_bp.route("/login", methods=["POST"])
def login_route():
    email, password = credentials_from_request()
    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({"error": "Email and password are required"}), 400

    api_key = login(email.strip().lower(), password)
    if api_key is None:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"api_key": api_key}), 200

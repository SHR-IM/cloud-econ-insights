import secrets
from functools import wraps
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User

#password hashing
def hash_password(password: str) -> str:
    """Return a hashed password."""
    return generate_password_hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a user's password."""
    return check_password_hash(password_hash, password)


#api key generation
def generate_api_key() -> str:
    """Generate a secure random API key."""
    return secrets.token_hex(32)


#authentication decorator
def require_api_key(f):
    """Decorator to enforce API key authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")

        if not api_key:
            return jsonify({"error": "Missing API key"}), 401

        user = User.query.filter_by(api_key_hash=api_key).first()

        if not user:
            return jsonify({"error": "Invalid API key"}), 403

        return f(*args, **kwargs)

    return decorated

#user registration
def create_user(email: str, password: str, role: str = "analyst"):
    """Creates a new user with hashed password + API key."""
    password_hash = hash_password(password)
    api_key = generate_api_key()

    user = User(
        email=email,
        password_hash=password_hash,
        api_key_hash=api_key,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return {
        "email": user.email,
        "api_key": user.api_key_hash,
        "role": user.role
    }

#login 
def login(email: str, password: str):
    """Return API key if credentials are correct."""
    user = User.query.filter_by(email=email).first()

    if not user or not verify_password(password, user.password_hash):
        return None

    return user.api_key_hash

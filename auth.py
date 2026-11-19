"""API-key authentication helpers for the portfolio prototype."""
import hashlib
import secrets
from functools import wraps

from flask import g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from models import User, db


def hash_api_key(api_key: str) -> str:
    """Hash a high-entropy random API key before database storage."""
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def generate_api_key() -> str:
    return secrets.token_hex(32)


def require_api_key(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY", "").strip()
        if not api_key:
            return jsonify({"error": "Missing API key"}), 401

        user = User.query.filter_by(api_key_hash=hash_api_key(api_key)).first()
        if user is None:
            return jsonify({"error": "Invalid API key"}), 403

        g.current_user = user
        return func(*args, **kwargs)

    return decorated


def create_user(email: str, password: str) -> dict:
    """Create a user and return their plaintext API key *once*."""
    raw_key = generate_api_key()
    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        api_key_hash=hash_api_key(raw_key),
    )
    db.session.add(user)
    db.session.commit()
    return {
        "email": user.email,
        "api_key": raw_key,
        "created_at": user.created_at.isoformat(),
    }


def login(email: str, password: str) -> str | None:
    """Rotate the user's API key on login; older keys are invalidated."""
    user = User.query.filter_by(email=email).first()
    if user is None or not check_password_hash(user.password_hash, password):
        return None

    raw_key = generate_api_key()
    user.api_key_hash = hash_api_key(raw_key)
    db.session.commit()
    return raw_key

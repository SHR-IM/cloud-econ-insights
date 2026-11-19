"""User-scoped economic indicator API."""
from flask import Blueprint, g, jsonify, request

from auth import require_api_key
from models import Indicator, db

indicators_bp = Blueprint("indicators", __name__)


def indicator_to_dict(item):
    return {
        "id": item.id,
        "code": item.code,
        "name": item.name,
        "description": item.description,
    }


@indicators_bp.route("/", methods=["GET"])
@require_api_key
def get_indicators():
    indicators = Indicator.query.filter_by(user_id=g.current_user.id).all()
    return jsonify([indicator_to_dict(item) for item in indicators]), 200


@indicators_bp.route("/", methods=["POST"])
@require_api_key
def create_indicator():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    code = data.get("code")
    name = data.get("name")
    description = data.get("description")
    if (
        not isinstance(code, str)
        or not code.strip()
        or len(code) > 50
        or not isinstance(name, str)
        or not name.strip()
        or len(name) > 200
        or (description is not None and not isinstance(description, str))
    ):
        return jsonify({"error": "Valid indicator code and name are required"}), 400

    indicator = Indicator(
        code=code.strip(),
        name=name.strip(),
        description=description,
        user_id=g.current_user.id,
    )
    db.session.add(indicator)
    db.session.commit()
    return jsonify(indicator_to_dict(indicator)), 201

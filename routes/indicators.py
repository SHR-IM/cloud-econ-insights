from flask import Blueprint, jsonify, request, g
from auth import require_api_key
from models import Indicator, db

indicators_bp = Blueprint("indicators", __name__)

@indicators_bp.route("/", methods=["GET"])
@require_api_key
def get_indicators():
    indicators = Indicator.query.all()
    data = [{"id": i.id, "code": i.code, "name": i.name, "description": i.description} for i in indicators]
    return jsonify(data), 200


@indicators_bp.route("/", methods=["POST"])
@require_api_key
def create_indicator():
    data = request.get_json(silent=True) or {}

    code = data.get("code")
    name = data.get("name")
    description = data.get("description")

    if not code or not name:
        return jsonify({"error": "code and name are required"}), 400

    indicator = Indicator(
        code=code,
        name=name,
        description=description,
        user_id=g.current_user.id
    )
    db.session.add(indicator)
    db.session.commit()

    return jsonify({
        "id": indicator.id,
        "code": indicator.code,
        "name": indicator.name,
        "description": indicator.description
    }), 201

from flask import Blueprint, jsonify, request
from auth import require_api_key
from models import Indicator, db

indicators_bp = Blueprint("indicators", __name__)

@indicators_bp.route("/indicators", methods=["GET"])
@require_api_key
def get_indicators():
    indicators = Indicator.query.all()
    data = [{"id": i.id, "code": i.code, "name": i.name} for i in indicators]
    return jsonify(data)

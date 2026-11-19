"""User-scoped economic snapshot API."""
from flask import Blueprint, g, jsonify, request

from auth import require_api_key
from models import EconSnapshot, Indicator, db

snapshots_bp = Blueprint("snapshots", __name__)


def snapshot_to_dict(snapshot):
    return {
        "id": snapshot.id,
        "indicator_id": snapshot.indicator_id,
        "country": snapshot.country,
        "year": snapshot.year,
        "value": snapshot.value,
        "fetched_at": snapshot.fetched_at.isoformat() if snapshot.fetched_at else None,
    }


def owned_snapshot(snapshot_id):
    return EconSnapshot.query.filter_by(
        id=snapshot_id, user_id=g.current_user.id
    ).first_or_404()


@snapshots_bp.route("/", methods=["GET"])
@require_api_key
def list_snapshots():
    query = EconSnapshot.query.filter_by(user_id=g.current_user.id)

    indicator_id = request.args.get("indicator_id", type=int)
    country = request.args.get("country")
    year = request.args.get("year", type=int)

    if indicator_id is not None:
        query = query.filter(EconSnapshot.indicator_id == indicator_id)
    if country:
        query = query.filter(EconSnapshot.country == country.upper())
    if year is not None:
        query = query.filter(EconSnapshot.year == year)

    return jsonify([snapshot_to_dict(snapshot) for snapshot in query.all()]), 200


@snapshots_bp.route("/<int:snapshot_id>", methods=["GET"])
@require_api_key
def get_snapshot(snapshot_id):
    return jsonify(snapshot_to_dict(owned_snapshot(snapshot_id))), 200


@snapshots_bp.route("/", methods=["POST"])
@require_api_key
def create_snapshot():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    indicator_id = data.get("indicator_id")
    country = data.get("country")
    year = data.get("year")
    value = data.get("value")

    try:
        if isinstance(indicator_id, bool) or isinstance(year, bool):
            raise ValueError
        indicator_id = int(indicator_id)
        year = int(year)
        value = float(value) if value is not None else None
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid indicator_id, year or value"}), 400

    if not isinstance(country, str) or len(country.strip()) not in (2, 3):
        return jsonify({"error": "Country must be a 2- or 3-letter code"}), 400

    indicator = Indicator.query.filter_by(
        id=indicator_id, user_id=g.current_user.id
    ).first()
    if indicator is None:
        return jsonify({"error": "Indicator not found"}), 404

    snapshot = EconSnapshot(
        indicator_id=indicator_id,
        user_id=g.current_user.id,
        country=country.strip().upper(),
        year=year,
        value=value,
    )
    db.session.add(snapshot)
    db.session.commit()
    return jsonify(snapshot_to_dict(snapshot)), 201


@snapshots_bp.route("/<int:snapshot_id>", methods=["PUT"])
@require_api_key
def update_snapshot(snapshot_id):
    snapshot = owned_snapshot(snapshot_id)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    if "country" in data:
        country = data["country"]
        if not isinstance(country, str) or len(country.strip()) not in (2, 3):
            return jsonify({"error": "Invalid country"}), 400
        snapshot.country = country.strip().upper()

    if "year" in data:
        try:
            if isinstance(data["year"], bool):
                raise ValueError
            snapshot.year = int(data["year"])
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid year"}), 400

    if "value" in data:
        try:
            snapshot.value = float(data["value"]) if data["value"] is not None else None
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid value"}), 400

    db.session.commit()
    return jsonify(snapshot_to_dict(snapshot)), 200


@snapshots_bp.route("/<int:snapshot_id>", methods=["DELETE"])
@require_api_key
def delete_snapshot(snapshot_id):
    snapshot = owned_snapshot(snapshot_id)
    db.session.delete(snapshot)
    db.session.commit()
    return jsonify({"message": f"Snapshot {snapshot_id} deleted"}), 200

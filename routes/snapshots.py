from flask import Blueprint, request, jsonify, g
from models import db, EconSnapshot, Indicator
from auth import require_api_key

snapshots_bp = Blueprint("snapshots", __name__)


def snapshot_to_dict(s: EconSnapshot):
    return {
        "id": s.id,
        "indicator_id": s.indicator_id,
        "country": s.country,
        "year": s.year,
        "value": s.value,
        "fetched_at": s.fetched_at.isoformat() if s.fetched_at else None,
    }


@snapshots_bp.route("/", methods=["GET"])
@require_api_key
def list_snapshots():
    query = EconSnapshot.query

    indicator_id = request.args.get("indicator_id", type=int)
    country = request.args.get("country")
    year = request.args.get("year", type=int)

    if indicator_id is not None:
        query = query.filter(EconSnapshot.indicator_id == indicator_id)

    if country:
        query = query.filter(EconSnapshot.country == country)

    if year is not None:
        query = query.filter(EconSnapshot.year == year)

    snapshots = query.all()
    return jsonify([snapshot_to_dict(s) for s in snapshots]), 200


@snapshots_bp.route("/<int:snapshot_id>", methods=["GET"])
@require_api_key
def get_snapshot(snapshot_id):
    snapshot = EconSnapshot.query.get_or_404(snapshot_id)
    return jsonify(snapshot_to_dict(snapshot)), 200


@snapshots_bp.route("/", methods=["POST"])
@require_api_key
def create_snapshot():
    data = request.json or {}

    indicator_id = data.get("indicator_id")
    country = data.get("country")
    year = data.get("year")
    value = data.get("value")

    if indicator_id is None or not country or year is None:
        return jsonify({"error": "indicator_id, country and year are required"}), 400

    try:
        indicator_id = int(indicator_id)
        year = int(year)
    except (ValueError, TypeError):
        return jsonify({"error": "indicator_id and year must be integers"}), 400

    if value is not None:
        try:
            value = float(value)
        except (ValueError, TypeError):
            return jsonify({"error": "value must be a number"}), 400

    indicator = Indicator.query.get(indicator_id)
    if not indicator:
        return jsonify({"error": f"Indicator with id {indicator_id} not found"}), 404

    snapshot = EconSnapshot(
        indicator_id=indicator_id,
        user_id=g.current_user.id,
        country=str(country),
        year=year,
        value=value,
    )

    db.session.add(snapshot)
    db.session.commit()

    return jsonify(snapshot_to_dict(snapshot)), 201


@snapshots_bp.route("/<int:snapshot_id>", methods=["PUT"])
@require_api_key
def update_snapshot(snapshot_id):
    snapshot = EconSnapshot.query.get_or_404(snapshot_id)
    data = request.json or {}

    if "country" in data:
        snapshot.country = str(data["country"])

    if "year" in data:
        try:
            snapshot.year = int(data["year"])
        except (ValueError, TypeError):
            return jsonify({"error": "year must be an integer"}), 400

    if "value" in data:
        if data["value"] is None:
            snapshot.value = None
        else:
            try:
                snapshot.value = float(data["value"])
            except (ValueError, TypeError):
                return jsonify({"error": "value must be a number"}), 400

    db.session.commit()
    return jsonify(snapshot_to_dict(snapshot)), 200


@snapshots_bp.route("/<int:snapshot_id>", methods=["DELETE"])
@require_api_key
def delete_snapshot(snapshot_id):
    snapshot = EconSnapshot.query.get_or_404(snapshot_id)
    db.session.delete(snapshot)
    db.session.commit()
    return jsonify({"message": f"Snapshot {snapshot_id} deleted"}), 200

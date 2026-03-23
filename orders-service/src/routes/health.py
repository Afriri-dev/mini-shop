from flask import Blueprint, jsonify

health_bp = Blueprint("orders_health", __name__)

@health_bp.route("/health", methods=["GET"])
def health():
    return jsonify(service="orders-service", status="ok"), 200
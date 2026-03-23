from flask import Blueprint, jsonify

from src.db import get_db_connection

health_bp = Blueprint("auth_health", __name__)

@health_bp.route("/health", methods=["GET"])
def health():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchall()   # consommer le résultat
        cursor.close()
        conn.close()
        return jsonify(service="auth", db="ok", status="ok"), 200
    except Exception as e:
        return jsonify(service="auth", db="error", details=str(e)), 500
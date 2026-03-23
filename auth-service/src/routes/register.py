from flask import Blueprint, jsonify, request
from src.db import get_db_connection

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["POST"])
def register():
    """
    Inscription d'un nouvel utilisateur :
    - Vérifie si le username existe déjà
    - Si non, insère un nouvel utilisateur dans la table 'users'
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Vérifie si l'utilisateur existe déjà
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            return jsonify({"error": "User already exists"}), 409

        # Insère le nouvel utilisateur
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": "DB connection failed", "details": str(e)}), 500
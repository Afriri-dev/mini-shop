from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
import bcrypt
from src.db import get_db_connection

# Définition du blueprint pour /login
login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    """
    Vérifie les identifiants envoyés par l'utilisateur.
    - Cherche l'utilisateur dans la table 'users'
    - Vérifie le mot de passe avec bcrypt
    - Si correct, génère un JWT
    - Sinon, renvoie une erreur 401
    """
    data = request.get_json()
    email = data.get("email")       # on utilise l'email comme identifiant unique
    password = data.get("password")

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Récupère l'utilisateur par email
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return jsonify({"error": "Utilisateur introuvable"}), 404

        # Vérifie le mot de passe avec bcrypt
        if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
            return jsonify({"error": "Mot de passe incorrect"}), 401

        # Génère un vrai JWT avec flask-jwt-extended
        token = create_access_token(identity=user["id"])  # on met l'id comme identité

        return jsonify({"token": token}), 200

    except Exception as e:
        return jsonify({"error": "DB connection failed", "details": str(e)}), 500
import os
from flask import Flask, request, jsonify
import mysql.connector
import bcrypt
import jwt
import datetime
from flask_cors import CORS

# --- Initialisation de l'application ---
app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "supersecretkey")  # même clé que dans Orders service

# --- Lecture des secrets (Docker) ou variables d'environnement (local/test) ---
def get_secret(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception:
        return None

DB_PASSWORD = get_secret("/run/secrets/db_password") or os.getenv("DB_PASSWORD", "rootpassword")
DB_HOST = os.getenv("DB_HOST", "mysql-db")

# --- Connexion à la base MySQL ---
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user="root",
        password=DB_PASSWORD,
        database="shopdb"
    )


# --- Health check (pour CI/CD et monitoring) ---
@app.route("/auth/health", methods=["GET"])
def health():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(service="auth", db="ok", status="ok"), 200
    except Exception as e:
        return jsonify(service="auth", db="error", details=str(e)), 500

# --- Inscription ---
@app.route("/auth/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Requête invalide, JSON attendu"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Champs requis manquants"}), 400

    # Hash du mot de passe
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_pw)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    return jsonify({"message": "Utilisateur créé avec succès"}), 201

# --- Connexion ---
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if data:
        email = data.get("email")
        password = data.get("password")
    else:
        email = request.form.get("email")
        password = request.form.get("password")

    if not email or not password:
        return jsonify({"error": "Email et mot de passe requis"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        return jsonify({"error": "Mot de passe incorrect"}), 401

    token = jwt.encode(
        {"user_id": user["id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    return jsonify({
        "token": token,
        "redirect": f"http://localhost:8080/orders.html?token={token}"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import mysql.connector

# --- Initialisation de l'application ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "http://127.0.0.1:8080"]}})

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")  # même clé que dans auth-service

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
@app.route("/orders/health", methods=["GET"])
def health():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(service="orders", db="ok", status="ok"), 200
    except Exception as e:
        return jsonify(service="orders", db="error", details=str(e)), 500

# --- Vérification du token JWT ---
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except Exception as e:
        print("Erreur JWT:", e)
        return None

# --- Créer une commande ---
@app.route("/orders", methods=["POST"])
def create_order():
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user_id = verify_token(token)

        if not user_id:
            return jsonify({"error": "Token invalide ou expiré"}), 401

        data = request.get_json()
        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)

        if not product_id:
            return jsonify({"error": "product_id requis"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
    "INSERT INTO orders (user_id, product_id, quantity, status, created_at) VALUES (%s, %s, %s, %s, %s)",
    (user_id, product_id, quantity, "pending", datetime.datetime.utcnow())
    )
        conn.commit()
        order_id = cursor.lastrowid
        cursor.close()
        conn.close()

        order = {
            "id": order_id,
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity,
            "status": "en attente",
            "created_at": datetime.datetime.utcnow().isoformat()
        }

        return jsonify({"message": "✅ Commande créée", "order": order}), 201
    except Exception as e:
        print("Erreur create_order:", e)
        return jsonify({"error": str(e)}), 500

# --- Lister les commandes ---
@app.route("/orders", methods=["GET"])
def list_orders():
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user_id = verify_token(token)

        if not user_id:
            return jsonify({"error": "Token invalide ou expiré"}), 401

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
        user_orders = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(user_orders), 200
    except Exception as e:
        print("Erreur list_orders:", e)
        return jsonify({"error": str(e)}), 500

# --- Récupérer une commande ---
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user_id = verify_token(token)

        if not user_id:
            return jsonify({"error": "Token invalide ou expiré"}), 401

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE id = %s AND user_id = %s", (order_id, user_id))
        order = cursor.fetchone()
        cursor.close()
        conn.close()

        if not order:
            return jsonify({"error": "Commande introuvable ou non autorisée"}), 404

        return jsonify(order), 200
    except Exception as e:
        print("Erreur get_order:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
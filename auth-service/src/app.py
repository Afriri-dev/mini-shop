from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Connexion MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="mysql-db",
        user="root",
        password="rootpassword",
        database="shopdb"
    )

@app.route("/")
def home():
    return "Auth Service OK"

@app.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": f"User {username} registered successfully!"})

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return jsonify({"message": f"User {username} logged in successfully!"})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    print("Routes enregistrées :", app.url_map)
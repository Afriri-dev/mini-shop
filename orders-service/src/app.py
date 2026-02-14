from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="mysql-db",
        user="root",
        password="rootpassword",
        database="shopdb"
    )

@app.route("/orders", methods=["GET"])
def get_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(orders)

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (user_id, product_id, quantity) VALUES (%s, %s, %s)",
        (user_id, product_id, quantity)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Order created successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
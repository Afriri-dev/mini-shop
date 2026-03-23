"""
Test d'intégration DB - nécessite MySQL (docker-compose ou CI services).
"""
import os
import pytest
import mysql.connector

def test_users_table_exists():
    """Vérifie que la table users existe (après init.sql)."""
    host = os.getenv("DB_HOST", "mysql-db")
    password = os.getenv("DB_PASSWORD", "rootpassword")
    try:
        conn = mysql.connector.connect(
            host=host,
            user="root",
            password=password,
            database="shopdb"
        )
    except Exception:
        pytest.skip("MySQL non disponible - lancer docker-compose up -d mysql-db")

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES LIKE 'users'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    assert result is not None, "La table 'users' n'a pas été créée par init.sql"
import os

def _get_db_password():
    """Lit le mot de passe depuis Docker secret ou variable d'environnement."""
    path = os.getenv("DB_PASSWORD_FILE", "/run/secrets/db_password")
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception:
        return os.getenv("DB_PASSWORD", "rootpassword")

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "devsecret123")
    DB_HOST = os.getenv("DB_HOST", "mysql-db")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = _get_db_password()
    DB_NAME = os.getenv("DB_NAME", "shopdb")
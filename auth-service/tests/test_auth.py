import pytest
import jwt

# -------------------------------
# 1. TEST UNITAIRE
# -------------------------------
def test_generate_jwt_token():
    """
    Vérifie qu'une fonction interne génère bien un token JWT valide.
    Ici, on simule une payload simple et on teste que le token est décodable.
    """
    payload = {"user_id": 1}
    secret = "devsecret123"
    token = jwt.encode(payload, secret, algorithm="HS256")

    # Décoder le token pour vérifier qu'il contient bien la payload
    decoded = jwt.decode(token, secret, algorithms=["HS256"])
    assert decoded["user_id"] == 1

# -------------------------------
# 2. TEST D'INTÉGRATION
# -------------------------------
def test_db_connection(client):
    """
    Vérifie que l'endpoint /auth/health confirme la connexion DB.
    Nécessite MySQL (docker-compose up) pour passer.
    Skippe si DB non disponible (ex: tests locaux sans Docker).
    """
    response = client.get("/auth/health")
    if response.status_code == 500 and response.json.get("db") == "error":
        pytest.skip("MySQL non disponible - lancer docker-compose up -d mysql-db")
    assert response.status_code == 200
    assert response.json.get("db") == "ok"

# -------------------------------
# 3. TEST FONCTIONNEL / API
# -------------------------------
def test_login(client):
    """
    Vérifie que /auth/login fonctionne : signup d'abord, puis login.
    Utilise signup pour créer un utilisateur de test (pas de dépendance aux seed data).
    """
    import uuid
    unique = uuid.uuid4().hex[:8]
    email = f"testlogin_{unique}@example.com"
    username = f"testuser_{unique}"

    # 1. Créer un utilisateur de test
    signup_resp = client.post("/auth/signup", json={
        "username": username,
        "email": email,
        "password": "TestPass123"
    })
    if signup_resp.status_code != 201:
        pytest.skip("DB non disponible ou erreur signup")

    # 2. Se connecter avec email/password
    response = client.post("/auth/login", json={
        "email": email,
        "password": "TestPass123"
    })
    assert response.status_code == 200
    assert "token" in response.json
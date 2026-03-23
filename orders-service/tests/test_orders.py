"""
Tests du service Orders.
Les tests unitaires ne nécessitent pas de DB.
Les tests d'intégration (health) nécessitent MySQL.
"""
def test_health_endpoint(client):
    """Vérifie que /orders/health répond (200 si DB ok, 500 sinon)."""
    response = client.get("/orders/health")
    assert response.status_code in (200, 500)
    data = response.json
    assert "service" in data
    assert data["service"] == "orders"
    if response.status_code == 200:
        assert data.get("db") == "ok"


def test_orders_requires_auth(client):
    """Vérifie que GET /orders sans token renvoie 401."""
    response = client.get("/orders")
    assert response.status_code == 401
    err = response.json.get("error", "")
    assert err  # message d'erreur présent

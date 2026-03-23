"""
Fixtures partagées pour les tests Orders.
"""
import pytest
from src.app import app


@pytest.fixture
def client():
    """Client de test Flask pour l'app Orders."""
    app.testing = True
    return app.test_client()

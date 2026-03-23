"""
Fixtures partagées pour les tests Auth.
"""
import pytest
from src.app import app


@pytest.fixture
def client():
    """Client de test Flask pour l'app Auth."""
    app.testing = True
    return app.test_client()

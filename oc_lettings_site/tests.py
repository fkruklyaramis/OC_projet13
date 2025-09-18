"""
Tests pour l'application oc_lettings_site.

Ce module contient tous les tests pour les vues principales
de l'application oc_lettings_site.
"""
import pytest
from django.urls import reverse
from django.test import Client


@pytest.fixture
def client():
    """Fixture pour le client de test Django."""
    return Client()


@pytest.mark.django_db
class TestMainViews:
    """Tests pour les vues principales de l'application."""

    def test_home_view(self, client):
        """Test la vue home."""
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert 'Welcome to Holiday Homes' in response.content.decode()
        assert 'Profiles' in response.content.decode()
        assert 'Lettings' in response.content.decode()


class TestMainURLs:
    """Tests pour les URLs principales de l'application."""

    def test_home_url(self):
        """Test l'URL home."""
        url = reverse('home')
        assert url == '/'

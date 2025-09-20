"""
Tests pour l'application oc_lettings_site.

Ce module contient tous les tests pour les vues principales
de l'application oc_lettings_site.
"""
import pytest
from unittest.mock import patch
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

    @patch('oc_lettings_site.views.logger')
    def test_home_view_logging(self, mock_logger, client):
        """Test que les logs sont appelés correctement dans la vue home."""
        response = client.get(reverse('home'))
        assert response.status_code == 200

        # Vérifier que le log a été appelé
        mock_logger.info.assert_called_once_with("Page d'accueil visitée par 127.0.0.1")

    @patch('oc_lettings_site.views.render')
    @patch('oc_lettings_site.views.logger')
    def test_home_view_exception_handling(self, mock_logger, mock_render, client):
        """Test la gestion d'exception dans la vue home."""
        # Simuler une exception
        mock_render.side_effect = Exception("Template error")

        with pytest.raises(Exception):
            client.get(reverse('home'))

        # Vérifier que l'erreur a été loggée
        expected_message = "Erreur lors du rendu de la page d'accueil: Template error"
        mock_logger.error.assert_called_once_with(expected_message)


class TestMainURLs:
    """Tests pour les URLs principales de l'application."""

    def test_home_url(self):
        """Test l'URL home."""
        url = reverse('home')
        assert url == '/'

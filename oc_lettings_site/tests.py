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
    """
    Fixture pytest fournissant un client de test Django configuré.

    Cette fixture crée une instance de django.test.Client qui simule
    un navigateur web pour les tests d'intégration des vues.

    Returns:
        Client: Instance du client de test Django
                - Supporte GET, POST, PUT, DELETE, etc.
                - Gère automatiquement les cookies et sessions
                - Permet de tester les réponses HTTP complètes

    Usage:
        @pytest.mark.django_db
        def test_my_view(client):
            response = client.get('/some-url/')
            assert response.status_code == 200

    Scope:
        Function-scoped : une nouvelle instance par test

    Dependencies:
        - pytest-django pour l'intégration Django
        - Base de données de test (via @pytest.mark.django_db)
    """
    return Client()


@pytest.mark.django_db
class TestMainViews:
    """
    Suite de tests pour les vues principales de l'application oc_lettings_site.

    Cette classe teste le comportement de la page d'accueil, incluant :
    - Accessibilité et codes de statut HTTP
    - Présence du contenu attendu dans les templates
    - Gestion des erreurs et logging
    - Comportement en cas d'exceptions

    Attributes:
        django_db: Marque pytest pour accès à la base de données de test

    Test Coverage:
        - Vue home() : page d'accueil principale
        - Template rendering et contenu
        - Logging des accès et erreurs
        - Gestion d'exceptions robuste

    Test Database:
        Utilise une base de données SQLite en mémoire créée/détruite
        automatiquement par pytest-django pour chaque test.
    """

    def test_home_view(self, client):
        """
        Test de la vue home() - page d'accueil du site.

        Vérifie que la page d'accueil :
        1. Est accessible (status 200)
        2. Contient les éléments de navigation attendus
        3. Affiche le titre de bienvenue correct

        Args:
            client (Client): Fixture du client de test Django

        Assertions:
            - Status code 200 (succès HTTP)
            - Présence du titre "Welcome to Holiday Homes"
            - Liens vers sections "Profiles" et "Lettings"

        URL testée:
            '/' (racine du site, nom='home')

        Template:
            oc_lettings_site/index.html
        """
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

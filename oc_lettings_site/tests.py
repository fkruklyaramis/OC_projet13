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

    @patch('oc_lettings_site.views.sentry_sdk')
    @patch('oc_lettings_site.views.render')
    @patch('oc_lettings_site.views.logger')
    def test_home_view_exception_handling(self, mock_logger, mock_render, mock_sentry, client):
        """Test la gestion d'exception dans la vue home."""
        # Simuler une exception
        mock_render.side_effect = Exception("Template error")

        with pytest.raises(Exception):
            client.get(reverse('home'))

        # Vérifier que l'erreur a été loggée dans la vue home spécifiquement
        expected_message = "Erreur lors du rendu de la page d'accueil: Template error"

        # Vérifier que le message attendu est dans les appels
        error_calls = mock_logger.error.call_args_list
        expected_call_found = any(
            call[0][0] == expected_message for call in error_calls
        )
        assert expected_call_found, f"Message attendu non trouvé dans les appels: {error_calls}"

    @patch('oc_lettings_site.views.sentry_sdk')
    @patch('oc_lettings_site.views.logger')
    def test_sentry_test_views_debug_mode(self, mock_logger, mock_sentry, client, settings):
        """Test les vues de test Sentry en mode DEBUG."""
        settings.DEBUG = True

        # Test vue 404 - retourne 404 car Django gère l'exception Http404
        response = client.get('/test-404/')
        assert response.status_code == 404
        mock_logger.warning.assert_called()

        # Reset mocks
        mock_logger.reset_mock()
        mock_sentry.reset_mock()

        # Test vue 500 - lève une exception non gérée
        try:
            response = client.get('/test-500/')
            # Si pas d'exception, vérifier le status 500
            assert response.status_code == 500
        except Exception:
            # C'est normal que l'exception soit levée
            pass
        mock_logger.error.assert_called()

    @patch('oc_lettings_site.views.sentry_sdk')
    def test_sentry_test_views_production_mode(self, mock_sentry, client, settings):
        """Test les vues de test Sentry en mode production (DEBUG=False)."""
        settings.DEBUG = False

        # En production, ces vues doivent retourner 404
        response = client.get('/test-404/')
        assert response.status_code == 404

        response = client.get('/test-500/')
        assert response.status_code == 404

        response = client.get('/test-sentry/')
        assert response.status_code == 404

    @patch.dict('os.environ', {}, clear=True)
    @patch('oc_lettings_site.views.sentry_sdk')
    def test_sentry_manual_no_dsn(self, mock_sentry, client, settings):
        """Test la vue test_sentry_manual sans DSN configurée."""
        settings.DEBUG = True

        response = client.get('/test-sentry/')
        assert response.status_code == 200
        assert 'Sentry non configuré' in response.content.decode()
        assert 'SENTRY_DSN' in response.content.decode()

    @patch.dict('os.environ', {'SENTRY_DSN': 'https://test@sentry.io/123'})
    @patch('oc_lettings_site.views.sentry_sdk')
    def test_sentry_manual_with_dsn(self, mock_sentry, client, settings):
        """Test la vue test_sentry_manual avec DSN configurée."""
        settings.DEBUG = True

        response = client.get('/test-sentry/')
        assert response.status_code == 200

        content = response.content.decode()
        assert 'Test Sentry Manuel' in content
        assert 'https://test@sentry.io/123' in content
        assert 'Message WARNING (404) envoyé' in content
        assert 'Message ERROR (500) envoyé' in content
        assert 'Exception capturée et envoyée' in content

        # Vérifier que les appels Sentry ont été faits
        assert mock_sentry.capture_message.call_count == 2
        assert mock_sentry.capture_exception.call_count == 1

    @patch.dict('os.environ', {'SENTRY_DSN': 'https://test@sentry.io/123'})
    @patch('oc_lettings_site.views.sentry_sdk')
    def test_sentry_manual_with_sentry_error(self, mock_sentry, client, settings):
        """Test la vue test_sentry_manual quand Sentry lève une erreur."""
        settings.DEBUG = True

        # Simuler une erreur Sentry
        mock_sentry.capture_message.side_effect = Exception("Sentry error")
        mock_sentry.capture_exception.side_effect = Exception("Sentry error")

        response = client.get('/test-sentry/')
        assert response.status_code == 200

        content = response.content.decode()
        assert 'Test Sentry Manuel' in content
        # Vérifier que les erreurs sont gérées gracieusement
        assert 'Erreur WARNING:' in content or 'Erreur ERROR:' in content


class TestMainURLs:
    """Tests pour les URLs principales de l'application."""

    def test_home_url(self):
        """Test l'URL home."""
        url = reverse('home')
        assert url == '/'

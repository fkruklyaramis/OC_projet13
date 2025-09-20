"""
Tests pour l'application lettings.

Ce module contient tous les tests pour les modèles, vues et URLs
de l'application lettings.
"""
import pytest
from unittest.mock import patch
from django.urls import reverse
from django.test import Client
from lettings.models import Address, Letting


@pytest.fixture
def client():
    """Fixture pour le client de test Django."""
    return Client()


@pytest.fixture
def address():
    """Fixture pour créer une adresse de test."""
    return Address.objects.create(
        number=123,
        street='Main Street',
        city='Anytown',
        state='CA',
        zip_code=12345,
        country_iso_code='USA'
    )


@pytest.fixture
def letting(address):
    """Fixture pour créer une location de test."""
    return Letting.objects.create(
        title='Test Letting',
        address=address
    )


@pytest.mark.django_db
class TestAddressModel:
    """Tests pour le modèle Address."""

    def test_address_str(self, address):
        """Test la méthode __str__ du modèle Address."""
        expected = '123 Main Street, Anytown'
        assert str(address) == expected

    def test_address_fields(self, address):
        """Test que tous les champs de l'adresse sont correctement sauvegardés."""
        assert address.number == 123
        assert address.street == 'Main Street'
        assert address.city == 'Anytown'
        assert address.state == 'CA'
        assert address.zip_code == 12345
        assert address.country_iso_code == 'USA'

    def test_verbose_name_plural(self):
        """Test que la pluralisation est correcte."""
        assert Address._meta.verbose_name_plural == 'Addresses'


@pytest.mark.django_db
class TestLettingModel:
    """Tests pour le modèle Letting."""

    def test_letting_str(self, letting):
        """Test la méthode __str__ du modèle Letting."""
        assert str(letting) == 'Test Letting'

    def test_letting_address_relationship(self, letting, address):
        """Test la relation OneToOne avec Address."""
        assert letting.address == address

    def test_verbose_name_plural(self):
        """Test que la pluralisation est correcte."""
        assert Letting._meta.verbose_name_plural == 'Lettings'


@pytest.mark.django_db
class TestLettingsViews:
    """Tests pour les vues de l'application lettings."""

    def test_index_view(self, client, letting):
        """Test la vue index des lettings."""
        response = client.get(reverse('lettings:index'))
        assert response.status_code == 200
        assert 'Lettings' in response.content.decode()
        assert 'Test Letting' in response.content.decode()

    def test_letting_detail_view(self, client, letting):
        """Test la vue détail d'un letting."""
        response = client.get(
            reverse('lettings:letting', kwargs={'letting_id': letting.id})
        )
        assert response.status_code == 200
        assert 'Test Letting' in response.content.decode()
        assert '123 Main Street' in response.content.decode()
        assert 'Anytown' in response.content.decode()

    def test_letting_detail_view_404(self, client):
        """Test la vue détail d'un letting inexistant."""
        response = client.get(
            reverse('lettings:letting', kwargs={'letting_id': 9999})
        )
        assert response.status_code == 404

    @patch('lettings.views.logger')
    def test_index_view_logging(self, mock_logger, client, letting):
        """Test que les logs sont appelés correctement dans la vue index."""
        response = client.get(reverse('lettings:index'))
        assert response.status_code == 200

        # Vérifier que les logs ont été appelés
        assert mock_logger.info.call_count == 2
        mock_logger.info.assert_any_call("Accès à la liste des lettings par 127.0.0.1")
        mock_logger.info.assert_any_call("Récupération de 1 lettings")

    @patch('lettings.views.logger')
    def test_letting_detail_view_logging(self, mock_logger, client, letting):
        """Test que les logs sont appelés correctement dans la vue détail."""
        response = client.get(
            reverse('lettings:letting', kwargs={'letting_id': letting.id})
        )
        assert response.status_code == 200

        # Vérifier que les logs ont été appelés
        assert mock_logger.info.call_count == 2
        mock_logger.info.assert_any_call("Accès au letting ID 1 par 127.0.0.1")
        mock_logger.info.assert_any_call("Letting 'Test Letting' récupéré avec succès")

    @patch('lettings.views.logger')
    def test_letting_detail_view_404_logging(self, mock_logger, client):
        """Test que les logs d'avertissement sont appelés pour une 404."""
        response = client.get(
            reverse('lettings:letting', kwargs={'letting_id': 9999})
        )
        assert response.status_code == 404

        # Vérifier que le log warning a été appelé
        mock_logger.warning.assert_called_once_with("Letting avec l'ID 9999 introuvable - 404")

    @patch('lettings.models.Letting.objects.all')
    @patch('lettings.views.logger')
    def test_index_view_exception_handling(self, mock_logger, mock_all, client):
        """Test la gestion d'exception dans la vue index."""
        # Simuler une exception
        mock_all.side_effect = Exception("Database error")

        with pytest.raises(Exception):
            client.get(reverse('lettings:index'))

        # Vérifier que l'erreur a été loggée
        mock_logger.error.assert_called_once_with("Erreur lors de la récupération des lettings: Database error")

    @patch('lettings.views.get_object_or_404')
    @patch('lettings.views.logger')
    def test_letting_detail_view_exception_handling(self, mock_logger, mock_get, client):
        """Test la gestion d'exception dans la vue détail."""
        # Simuler une exception (autre que Http404)
        mock_get.side_effect = Exception("Database connection error")

        with pytest.raises(Exception):
            client.get(reverse('lettings:letting', kwargs={'letting_id': 1}))

        # Vérifier que l'erreur a été loggée
        expected_message = "Erreur lors de la récupération du letting 1: Database connection error"
        mock_logger.error.assert_called_once_with(expected_message)


@pytest.mark.django_db
class TestLettingsURLs:
    """Tests pour les URLs de l'application lettings."""

    def test_index_url(self):
        """Test l'URL index des lettings."""
        url = reverse('lettings:index')
        assert url == '/lettings/'

    def test_letting_detail_url(self, letting):
        """Test l'URL détail d'un letting."""
        url = reverse('lettings:letting', kwargs={'letting_id': letting.id})
        assert url == f'/lettings/{letting.id}/'

"""
Tests pour l'application profiles.

Ce module contient tous les tests pour les modèles, vues et URLs
de l'application profiles.
"""
import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from profiles.models import Profile


@pytest.fixture
def client():
    """Fixture pour le client de test Django."""
    return Client()


@pytest.fixture
def user():
    """Fixture pour créer un utilisateur de test."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='John',
        last_name='Doe'
    )


@pytest.fixture
def profile(user):
    """Fixture pour créer un profil de test."""
    return Profile.objects.create(
        user=user,
        favorite_city='Paris'
    )


@pytest.mark.django_db
class TestProfileModel:
    """Tests pour le modèle Profile."""

    def test_profile_str(self, profile):
        """Test la méthode __str__ du modèle Profile."""
        assert str(profile) == 'testuser'

    def test_profile_user_relationship(self, profile, user):
        """Test la relation OneToOne avec User."""
        assert profile.user == user
        assert profile.favorite_city == 'Paris'

    def test_verbose_name_plural(self):
        """Test que la pluralisation est correcte."""
        assert Profile._meta.verbose_name_plural == 'Profiles'

    def test_profile_favorite_city_blank(self):
        """Test qu'un profil peut être créé sans favorite_city."""
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        profile2 = Profile.objects.create(
            user=user2,
            favorite_city=''
        )
        assert profile2.favorite_city == ''


@pytest.mark.django_db
class TestProfilesViews:
    """Tests pour les vues de l'application profiles."""

    def test_index_view(self, client, profile):
        """Test la vue index des profiles."""
        response = client.get(reverse('profiles:index'))
        assert response.status_code == 200
        assert 'Profiles' in response.content.decode()
        assert 'testuser' in response.content.decode()

    def test_profile_detail_view(self, client, profile, user):
        """Test la vue détail d'un profile."""
        response = client.get(
            reverse('profiles:profile', kwargs={'username': user.username})
        )
        assert response.status_code == 200
        assert 'testuser' in response.content.decode()
        assert 'John' in response.content.decode()
        assert 'Doe' in response.content.decode()
        assert 'Paris' in response.content.decode()

    def test_profile_detail_view_404(self, client):
        """Test la vue détail d'un profile inexistant."""
        response = client.get(
            reverse('profiles:profile', kwargs={'username': 'nonexistent'})
        )
        assert response.status_code == 404


@pytest.mark.django_db
class TestProfilesURLs:
    """Tests pour les URLs de l'application profiles."""

    def test_index_url(self):
        """Test l'URL index des profiles."""
        url = reverse('profiles:index')
        assert url == '/profiles/'

    def test_profile_detail_url(self, user):
        """Test l'URL détail d'un profile."""
        url = reverse('profiles:profile', kwargs={'username': user.username})
        assert url == f'/profiles/{user.username}/'

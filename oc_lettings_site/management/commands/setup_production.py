"""
/Users/frakrukly/Documents/OC/repo/OC_projet13/oc_lettings_site/management/commands/setup_production.py

Commande Django pour initialiser les données de production automatiquement.
Crée un superuser et des données de démonstration si elles n'existent pas.
"""
import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from lettings.models import Letting, Address
from profiles.models import Profile


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Commande Django pour l'initialisation automatique des données de production.

    Cette commande crée automatiquement un superuser administrateur et des données
    de démonstration (utilisateurs, profils, adresses et lettings) si elles
    n'existent pas déjà dans la base de données.

    Utilisée principalement lors du déploiement Docker pour garantir que
    l'application a des données initiales fonctionnelles.

    Attributes:
        help (str): Description de la commande affichée dans --help

    Examples:
        python manage.py setup_production
        python manage.py setup_production --force
    """

    help = 'Setup automatique du superuser et des données de démonstration pour la production'

    def add_arguments(self, parser):
        """
        Ajouter les arguments de ligne de commande disponibles.

        Args:
            parser (ArgumentParser): Parser d'arguments Django

        Note:
            --force : Force la recréation des données même si elles existent
        """
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force la recréation des données même si elles existent'
        )

    def handle(self, *args, **options):
        """
        Point d'entrée principal de la commande Django.

        Exécute le processus complet d'initialisation des données de production :
        1. Création du superuser administrateur
        2. Création des données de démonstration (utilisateurs, profils, lettings)

        Args:
            *args: Arguments positionnels (non utilisés)
            **options: Options de la commande
                - force (bool): Si True, force la recréation des données existantes

        Raises:
            Exception: En cas d'erreur lors du setup, loggée et re-lancée

        Returns:
            None

        Side Effects:
            - Crée des enregistrements en base de données
            - Affiche des messages de progression sur stdout
            - Enregistre des logs via le logger
        """
        self.stdout.write(self.style.SUCCESS('Démarrage du setup production...'))

        try:
            # Créer le superuser
            self._create_superuser(options.get('force', False))

            # Créer les données de démonstration
            self._create_demo_data(options.get('force', False))

            self.stdout.write(self.style.SUCCESS('Setup production terminé avec succès !'))

        except Exception as e:
            logger.error(f"Erreur lors du setup production: {e}")
            self.stdout.write(
                self.style.ERROR(f'Erreur lors du setup: {e}')
            )
            raise

    def _create_superuser(self, force=False):
        """
        Créer le superuser administrateur pour l'application.

        Crée un compte administrateur avec les identifiants par défaut si il n'existe
        pas déjà. En mode force, supprime et recrée le superuser existant.

        Args:
            force (bool): Si True, supprime et recrée le superuser même s'il existe.
                         Si False (défaut), ignore si le superuser existe déjà.

        Returns:
            None

        Side Effects:
            - Crée un User avec is_superuser=True en base de données
            - Affiche des messages informatifs sur stdout
            - Enregistre des logs via le logger
            - En mode force : supprime le superuser existant

        Note:
            Identifiants par défaut :
            - Username: admin
            - Password: admin  # À changer en production réelle
            - Email: admin@oc-lettings.com
        """
        username = 'admin'
        email = 'admin@oc-lettings.com'
        password = 'admin'  # En production, utiliser une variable d'environnement

        if User.objects.filter(username=username).exists():
            if not force:
                self.stdout.write(f'ℹ️  Superuser "{username}" existe déjà')
                return
            else:
                User.objects.filter(username=username).delete()
                self.stdout.write(f'Suppression et recréation du superuser "{username}"')

        # Créer le superuser
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(f'Superuser créé: {username} / {password}')
        )
        logger.info(f"Superuser créé: {username}")

    def _create_demo_data(self, force=False):
        """
        Créer un jeu complet de données de démonstration pour l'application.

        Génère des utilisateurs, profils, adresses et lettings de test pour permettre
        une démonstration fonctionnelle de l'application sans données réelles.

        Données créées :
        - 4 utilisateurs normaux avec profils associés
        - 4 adresses dans différentes villes
        - 4 lettings correspondants aux adresses

        Args:
            force (bool): Si True, supprime toutes les données existantes avant création.
                         Si False (défaut), ignore si des données existent déjà.

        Returns:
            None

        Side Effects:
            - Crée des enregistrements User, Profile, Address, Letting en base
            - En mode force : supprime TOUTES les données existantes (ATTENTION!)
            - Affiche un résumé des créations sur stdout
            - Enregistre des logs de succès

        Warning:
            Le mode force supprime TOUTES les données utilisateurs existantes
            (sauf les superusers). À utiliser avec précaution.

        Data Structure:
            Utilisateurs créés :
            - john_doe (Paris), jane_smith (London)
            - bob_wilson (New York), alice_brown (Tokyo)

            Lettings créés :
            - "Cozy Downtown Apartment" (Paris)
            - "Modern Loft in City Center" (London)
            - "Sunny Beach House" (Miami)
            - "Mountain View Cabin" (Denver)
        """
        if not force and (Letting.objects.exists() or Profile.objects.exists()):
            self.stdout.write('ℹ️  Données de démonstration déjà présentes')
            return

        if force:
            # Supprimer les données existantes
            Letting.objects.all().delete()
            Address.objects.all().delete()
            Profile.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write('Suppression des données existantes')

        # Créer des utilisateurs normaux
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'bob_wilson', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Wilson'},
            {'username': 'alice_brown', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Brown'},
        ]

        created_users = []
        for user_data in users_data:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password='demo123',
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            created_users.append(user)

        self.stdout.write(f'{len(created_users)} utilisateurs créés')

        # Créer des profils
        profiles_data = [
            {'user': created_users[0], 'favorite_city': 'Paris'},
            {'user': created_users[1], 'favorite_city': 'London'},
            {'user': created_users[2], 'favorite_city': 'New York'},
            {'user': created_users[3], 'favorite_city': 'Tokyo'},
        ]

        created_profiles = []
        for profile_data in profiles_data:
            profile = Profile.objects.create(**profile_data)
            created_profiles.append(profile)

        self.stdout.write(f'{len(created_profiles)} profils créés')

        # Créer des adresses et lettings
        lettings_data = [
            {
                'title': 'Cozy Downtown Apartment',
                'address': {'number': 123, 'street': 'Main Street', 'city': 'Paris',
                            'state': 'IL', 'zip_code': 75001, 'country_iso_code': 'FR'}
            },
            {
                'title': 'Modern Loft in City Center',
                'address': {'number': 456, 'street': 'Oak Avenue', 'city': 'London',
                            'state': 'CA', 'zip_code': 90210, 'country_iso_code': 'UK'}
            },
            {
                'title': 'Sunny Beach House',
                'address': {'number': 789, 'street': 'Beach Road', 'city': 'Miami',
                            'state': 'FL', 'zip_code': 33101, 'country_iso_code': 'US'}
            },
            {
                'title': 'Mountain View Cabin',
                'address': {'number': 321, 'street': 'Mountain Trail', 'city': 'Denver',
                            'state': 'CO', 'zip_code': 80201, 'country_iso_code': 'US'}
            }
        ]

        created_lettings = []
        for letting_data in lettings_data:
            # Créer l'adresse
            address = Address.objects.create(**letting_data['address'])

            # Créer le letting
            letting = Letting.objects.create(
                title=letting_data['title'],
                address=address
            )
            created_lettings.append(letting)

        self.stdout.write(f'{len(created_lettings)} lettings créés')

        # Résumé
        self.stdout.write(
            self.style.SUCCESS(
                f'Données de démonstration créées:\n'
                f'   - {len(created_users)} utilisateurs\n'
                f'   - {len(created_profiles)} profils\n'
                f'   - {len(created_lettings)} lettings'
            )
        )

        logger.info("Données de démonstration créées avec succès")

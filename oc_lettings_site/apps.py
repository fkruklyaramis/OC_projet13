"""
Configuration de l'application principale oc_lettings_site.

Ce module définit la configuration Django pour l'application principale
qui gère les paramètres globaux du projet.
"""
from django.apps import AppConfig


class OCLettingsSiteConfig(AppConfig):
    """
    Configuration de l'application Django principale oc_lettings_site.

    Cette classe définit les paramètres de configuration pour l'application principale
    qui gère la page d'accueil et les URLs globales du projet.

    Attributes:
        name (str): Nom technique de l'application Django pour la configuration
                   et l'autodiscovery des modèles, migrations, etc.

    Note:
        Cette classe est automatiquement chargée par Django au démarrage
        via le paramètre default_app_config dans __init__.py ou INSTALLED_APPS.
    """

    name = 'oc_lettings_site'

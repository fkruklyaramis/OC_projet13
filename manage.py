"""
Script utilitaire de gestion Django pour oc_lettings_site.

Ce script est le point d'entrée principal pour toutes les commandes
d'administration Django : migrations, serveur de développement,
collecte de fichiers statiques, tests, etc.

Usage:
    python manage.py <command> [options]

Commandes courantes:
    runserver     : Lance le serveur de développement
    migrate       : Applique les migrations de base de données
    makemigrations: Crée les fichiers de migrations
    collectstatic : Collecte les fichiers statiques
    createsuperuser: Crée un compte administrateur
    test          : Lance les tests
    shell         : Ouvre un shell Python Django

Variables d'environnement:
    DJANGO_SETTINGS_MODULE: Module de configuration Django
                           (défaut: oc_lettings_site.settings)
"""
import os
import sys


def main():
    """
    Point d'entrée principal du script de gestion Django.

    Configure l'environnement Django et délègue l'exécution à
    django.core.management.execute_from_command_line qui parse
    les arguments et exécute la commande appropriée.

    Raises:
        ImportError: Si Django n'est pas installé ou accessible
                    Fournit un message d'aide pour le diagnostic

    Side Effects:
        - Configure DJANGO_SETTINGS_MODULE si non défini
        - Parse les arguments de ligne de commande (sys.argv)
        - Exécute la commande Django demandée

    Environment:
        Nécessite Django installé dans l'environnement Python actuel
        et le module de settings accessible via PYTHONPATH.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

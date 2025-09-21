"""
Configuration WSGI pour l'application oc_lettings_site.

Ce module expose l'application WSGI comme variable de niveau module nommée 'application'.
Il est utilisé par les serveurs web compatibles WSGI pour servir l'application Django
en mode production.

WSGI (Web Server Gateway Interface) est la spécification Python standard
pour l'interface entre serveurs web et applications web.

Usage:
    - Développement: python manage.py runserver (utilise ASGI par défaut Django 3.0+)
    - Production: gunicorn, uwsgi, mod_wsgi Apache, etc.

Variables d'environnement:
    DJANGO_SETTINGS_MODULE: Module de configuration Django à utiliser
                           (défaut: oc_lettings_site.settings)

Example:
    gunicorn --bind 0.0.0.0:8000 oc_lettings_site.wsgi:application
    uwsgi --http :8000 --module oc_lettings_site.wsgi:application
"""
import os

from django.core.wsgi import get_wsgi_application

# Configuration du module de settings Django
# Cette variable d'environnement doit pointer vers le module de configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')

# Création et exposition de l'application WSGI
# Cette variable est utilisée par les serveurs WSGI (gunicorn, uwsgi, etc.)
application = get_wsgi_application()

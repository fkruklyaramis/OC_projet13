"""
Module de configuration de l'interface d'administration pour l'application profiles.

Ce module configure l'affichage du modèle Profile
dans l'interface d'administration Django.
"""
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)

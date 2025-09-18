"""
Module de configuration de l'interface d'administration pour l'application lettings.

Ce module configure l'affichage des modèles Address et Letting
dans l'interface d'administration Django.
"""
from django.contrib import admin
from .models import Address, Letting

admin.site.register(Address)
admin.site.register(Letting)

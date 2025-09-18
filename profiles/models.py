"""
Module contenant les modèles pour l'application profiles.

Ce module définit le modèle Profile utilisé pour gérer
les profils utilisateur.
"""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Modèle représentant un profil utilisateur.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    class Meta:
        """
        Configuration des métadonnées du modèle Profile.
        """
        verbose_name_plural = "Profiles"

    def __str__(self):
        """
        Retourne le nom d'utilisateur du profil.
        """
        return self.user.username

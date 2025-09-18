"""
Module contenant les modèles pour l'application lettings.

Ce module définit les modèles Address et Letting utilisés
pour gérer les adresses et les locations.
"""
from django.db import models


class Address(models.Model):
    """
    Modèle représentant une adresse.
    """
    number = models.PositiveIntegerField(null=False)
    street = models.CharField(max_length=64, null=False)
    city = models.CharField(max_length=64, null=False)
    state = models.CharField(max_length=2, null=False)
    zip_code = models.PositiveIntegerField(null=False)
    country_iso_code = models.CharField(max_length=3, null=False)

    class Meta:
        """
        Configuration des métadonnées du modèle Address.
        """
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        """
        Retourne une représentation textuelle de l'adresse.
        """
        return f'{self.number} {self.street}, {self.city}'


class Letting(models.Model):
    """
    Modèle représentant une location.
    """
    title = models.CharField(max_length=256, null=False)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    class Meta:
        """
        Configuration des métadonnées du modèle Letting.
        """
        verbose_name_plural = "Lettings"

    def __str__(self):
        """
        Retourne le titre de la location.
        """
        return self.title

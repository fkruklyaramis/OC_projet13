"""
Module contenant les modèles pour l'application lettings.

Ce module définit les modèles Address et Letting utilisés
pour gérer les adresses et les locations.
"""
import logging
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


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


# Configuration des signaux pour le logging
logger = logging.getLogger('lettings')


@receiver(post_save, sender=Address)
def address_saved(sender, instance, created, **kwargs):
    """
    Signal déclenché après la sauvegarde d'une adresse.
    """
    if created:
        logger.info(f"Nouvelle adresse créée: {instance}")
    else:
        logger.info(f"Adresse mise à jour: {instance}")


@receiver(post_delete, sender=Address)
def address_deleted(sender, instance, **kwargs):
    """
    Signal déclenché après la suppression d'une adresse.
    """
    logger.warning(f"Adresse supprimée: {instance}")


@receiver(post_save, sender=Letting)
def letting_saved(sender, instance, created, **kwargs):
    """
    Signal déclenché après la sauvegarde d'un letting.
    """
    if created:
        logger.info(f"Nouveau letting créé: {instance.title}")
    else:
        logger.info(f"Letting mis à jour: {instance.title}")


@receiver(post_delete, sender=Letting)
def letting_deleted(sender, instance, **kwargs):
    """
    Signal déclenché après la suppression d'un letting.
    """
    logger.warning(f"Letting supprimé: {instance.title}")

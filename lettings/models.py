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
    Signal Django déclenché automatiquement après sauvegarde d'une adresse.

    Enregistre un log informatif pour tracer les opérations sur les adresses,
    importantes pour le référencement géographique des lettings.

    Args:
        sender (class): Classe du modèle qui a envoyé le signal (Address)
        instance (Address): Instance de l'adresse sauvegardée
        created (bool): True si l'adresse vient d'être créée, False si mise à jour
        **kwargs: Arguments supplémentaires du signal Django
                 - using: nom de la base de données utilisée
                 - update_fields: champs modifiés (si spécifié)

    Returns:
        None

    Side Effects:
        - Enregistre un log INFO avec représentation string de l'adresse
        - Log différencié selon création ou modification

    Connected To:
        post_save signal du modèle Address via @receiver decorator

    Business Logic:
        Les adresses sont critiques car liées 1:1 aux lettings.
        Toute modification peut impacter la localisation des biens.

    Example Logs:
        INFO - Nouvelle adresse créée: 123 Main Street, Paris, IL 75001, FR
        INFO - Adresse mise à jour: 123 Main Street, Paris, IL 75001, FR
    """
    if created:
        logger.info(f"Nouvelle adresse créée: {instance}")
    else:
        logger.info(f"Adresse mise à jour: {instance}")


@receiver(post_delete, sender=Address)
def address_deleted(sender, instance, **kwargs):
    """
    Signal Django déclenché automatiquement après suppression d'une adresse.

    Enregistre un log d'avertissement car la suppression d'une adresse
    peut causer des problèmes d'intégrité avec les lettings associés.

    Args:
        sender (class): Classe du modèle qui a envoyé le signal (Address)
        instance (Address): Instance de l'adresse supprimée (avant suppression)
        **kwargs: Arguments supplémentaires du signal Django
                 - using: nom de la base de données utilisée

    Returns:
        None

    Side Effects:
        - Enregistre un log WARNING avec représentation string de l'adresse

    Connected To:
        post_delete signal du modèle Address via @receiver decorator

    Warning:
        Une adresse supprimée peut laisser des lettings orphelins si la relation
        n'est pas correctement gérée (CASCADE). Ce log aide à détecter ces cas.

    Example Log:
        WARNING - Adresse supprimée: 123 Main Street, Paris, IL 75001, FR
    """
    logger.warning(f"Adresse supprimée: {instance}")


@receiver(post_save, sender=Letting)
def letting_saved(sender, instance, created, **kwargs):
    """
    Signal Django déclenché automatiquement après sauvegarde d'un letting.

    Enregistre un log informatif pour tracer les opérations sur les lettings,
    cœur métier de l'application de gestion immobilière.

    Args:
        sender (class): Classe du modèle qui a envoyé le signal (Letting)
        instance (Letting): Instance du letting sauvegardé
        created (bool): True si le letting vient d'être créé, False si mise à jour
        **kwargs: Arguments supplémentaires du signal Django
                 - using: nom de la base de données utilisée
                 - update_fields: champs modifiés (si spécifié)

    Returns:
        None

    Side Effects:
        - Enregistre un log INFO avec le titre du letting
        - Log différencié selon création ou modification

    Connected To:
        post_save signal du modèle Letting via @receiver decorator

    Business Impact:
        Les lettings sont les objets centraux de l'application.
        Leur traçabilité est essentielle pour l'audit et le monitoring business.

    Example Logs:
        INFO - Nouveau letting créé: Cozy Downtown Apartment
        INFO - Letting mis à jour: Cozy Downtown Apartment
    """
    if created:
        logger.info(f"Nouveau letting créé: {instance.title}")
    else:
        logger.info(f"Letting mis à jour: {instance.title}")


@receiver(post_delete, sender=Letting)
def letting_deleted(sender, instance, **kwargs):
    """
    Signal Django déclenché automatiquement après suppression d'un letting.

    Enregistre un log d'avertissement car la suppression d'un letting
    représente la perte d'un bien immobilier de l'inventaire.

    Args:
        sender (class): Classe du modèle qui a envoyé le signal (Letting)
        instance (Letting): Instance du letting supprimé (avant suppression)
        **kwargs: Arguments supplémentaires du signal Django
                 - using: nom de la base de données utilisée

    Returns:
        None

    Side Effects:
        - Enregistre un log WARNING avec le titre du letting

    Connected To:
        post_delete signal du modèle Letting via @receiver decorator

    Business Impact:
        La suppression d'un letting est un événement important qui peut
        indiquer une fin de contrat, vente, ou retrait du marché.
        Ce log permet un suivi business et audit.
    Example Log:
        WARNING - Letting supprimé: Cozy Downtown Apartment
    """
    logger.warning(f"Letting supprimé: {instance.title}")

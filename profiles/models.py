"""
Module contenant les modèles pour l'application profiles.

Ce module définit le modèle Profile utilisé pour gérer
les profils utilisateur.
"""
import logging
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


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


# Configuration des signaux pour le logging
logger = logging.getLogger('profiles')


@receiver(post_save, sender=Profile)
def profile_saved(sender, instance, created, **kwargs):
    """
    Signal Django déclenché automatiquement après sauvegarde d'un profil.

    Enregistre un log informatif pour tracer les opérations de création
    et modification des profils utilisateurs.

    Args:
        sender (class): Classe du modèle qui a envoyé le signal (Profile)
        instance (Profile): Instance du profil sauvegardé
        created (bool): True si l'instance vient d'être créée, False si mise à jour
        **kwargs: Arguments supplémentaires du signal Django
                 - using: nom de la base de données utilisée
                 - update_fields: champs mis à jour (si spécifié)

    Returns:
        None

    Side Effects:
        - Enregistre un log INFO avec le nom d'utilisateur
        - Log différencié selon création ou modification

    Connected To:
        post_save signal du modèle Profile via @receiver decorator

    Example Logs:
        INFO - Nouveau profil créé pour l'utilisateur: john_doe
        INFO - Profil mis à jour pour l'utilisateur: john_doe
    """
    if created:
        logger.info(f"Nouveau profil créé pour l'utilisateur: {instance.user.username}")
    else:
        logger.info(f"Profil mis à jour pour l'utilisateur: {instance.user.username}")


@receiver(post_delete, sender=Profile)
def profile_deleted(sender, instance, **kwargs):
    """
    Signal Django déclenché automatiquement après suppression d'un profil.

    Enregistre un log d'avertissement pour tracer les suppressions de profils,
    ce qui peut indiquer une désactivation de compte ou nettoyage de données.

    Args:
        sender (class): Classe du modèle qui a envoyé le signal (Profile)
        instance (Profile): Instance du profil supprimé (avant suppression)
        **kwargs: Arguments supplémentaires du signal Django
                 - using: nom de la base de données utilisée

    Returns:
        None

    Side Effects:
        - Enregistre un log WARNING avec le nom d'utilisateur

    Connected To:
        post_delete signal du modèle Profile via @receiver decorator

    Note:
        Ce signal se déclenche APRÈS la suppression en base, donc
        instance.user peut encore être accessible temporairement.

    Example Log:
        WARNING - Profil supprimé pour l'utilisateur: john_doe
    """
    logger.warning(f"Profil supprimé pour l'utilisateur: {instance.user.username}")


@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    """
    Signal Django déclenché automatiquement après sauvegarde d'un utilisateur.

    Enregistre un log informatif pour tracer les opérations de création et
    modification des comptes utilisateurs pour l'audit et le monitoring.

    Args:
        sender (class): Classe du modèle qui a envoyé le signal (User - Django auth)
        instance (User): Instance de l'utilisateur sauvegardé
        created (bool): True si l'utilisateur vient d'être créé, False si mise à jour
        **kwargs: Arguments supplémentaires du signal Django
                 - using: nom de la base de données utilisée
                 - update_fields: champs mis à jour (si spécifié)

    Returns:
        None

    Side Effects:
        - Enregistre un log INFO avec le nom d'utilisateur
        - Log différencié selon création ou modification de compte

    Connected To:
        post_save signal du modèle User de Django auth via @receiver decorator

    Security Note:
        Ce signal trace toutes les modifications de comptes, utile pour
        la sécurité et la détection d'activités suspectes.

    Example Logs:
        INFO - Nouvel utilisateur créé: john_doe
        INFO - Utilisateur mis à jour: john_doe
    """
    if created:
        logger.info(f"Nouvel utilisateur créé: {instance.username}")
    else:
        logger.info(f"Utilisateur mis à jour: {instance.username}")

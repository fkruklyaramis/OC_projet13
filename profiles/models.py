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
    Signal déclenché après la sauvegarde d'un profil.
    """
    if created:
        logger.info(f"Nouveau profil créé pour l'utilisateur: {instance.user.username}")
    else:
        logger.info(f"Profil mis à jour pour l'utilisateur: {instance.user.username}")


@receiver(post_delete, sender=Profile)
def profile_deleted(sender, instance, **kwargs):
    """
    Signal déclenché après la suppression d'un profil.
    """
    logger.warning(f"Profil supprimé pour l'utilisateur: {instance.user.username}")


@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    """
    Signal déclenché après la sauvegarde d'un utilisateur.
    """
    if created:
        logger.info(f"Nouvel utilisateur créé: {instance.username}")
    else:
        logger.info(f"Utilisateur mis à jour: {instance.username}")

"""
Module contenant les vues pour l'application profiles.

Ce module définit les vues pour afficher la liste des profils
et les détails d'un profil spécifique.
"""
import logging
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Profile

logger = logging.getLogger('profiles')


def index(request):
    """
    Affiche la liste des profils.

    Args:
        request: L'objet HttpRequest de Django.

    Returns:
        HttpResponse: La réponse HTTP avec le template rendu.
    """
    logger.info(f"Accès à la liste des profils par {request.META.get('REMOTE_ADDR', 'IP inconnue')}")

    try:
        profiles_list = Profile.objects.all()
        logger.info(f"Récupération de {len(profiles_list)} profils")
        context = {'profiles_list': profiles_list}
        return render(request, 'profiles/index.html', context)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des profils: {str(e)}")
        raise


def profile(request, username):
    """
    Affiche les détails d'un profil spécifique.

    Args:
        request: L'objet HttpRequest de Django.
        username: Le nom d'utilisateur du profil à afficher.

    Returns:
        HttpResponse: La réponse HTTP avec le template rendu.
    """
    logger.info(f"Accès au profil '{username}' par {request.META.get('REMOTE_ADDR', 'IP inconnue')}")

    try:
        profile = get_object_or_404(Profile, user__username=username)
        logger.info(f"Profil de {username} récupéré avec succès")

        context = {'profile': profile}
        return render(request, 'profiles/profile.html', context)

    except Http404:
        logger.warning(f"Profil '{username}' introuvable - 404")
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du profil {username}: {str(e)}")
        raise

"""
Module contenant les vues pour l'application lettings.

Ce module définit les vues pour afficher la liste des locations
et les détails d'une location spécifique.
"""
import logging
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Letting

logger = logging.getLogger('lettings')


def index(request):
    """
    Affiche la liste des locations.

    Args:
        request: L'objet HttpRequest de Django.

    Returns:
        HttpResponse: La réponse HTTP avec le template rendu.
    """
    logger.info(f"Accès à la liste des lettings par {request.META.get('REMOTE_ADDR', 'IP inconnue')}")

    try:
        lettings_list = Letting.objects.all()
        logger.info(f"Récupération de {len(lettings_list)} lettings")
        context = {'lettings_list': lettings_list}
        return render(request, 'lettings/index.html', context)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des lettings: {str(e)}")
        raise


def letting(request, letting_id):
    """
    Affiche les détails d'une location spécifique.

    Args:
        request: L'objet HttpRequest de Django.
        letting_id: L'identifiant de la location à afficher.

    Returns:
        HttpResponse: La réponse HTTP avec le template rendu.
    """
    logger.info(f"Accès au letting ID {letting_id} par {request.META.get('REMOTE_ADDR', 'IP inconnue')}")

    try:
        letting = get_object_or_404(Letting, id=letting_id)
        logger.info(f"Letting '{letting.title}' récupéré avec succès")

        context = {
            'title': letting.title,
            'address': letting.address,
        }
        return render(request, 'lettings/letting.html', context)

    except Http404:
        logger.warning(f"Letting avec l'ID {letting_id} introuvable - 404")
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du letting {letting_id}: {str(e)}")
        raise

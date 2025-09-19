"""
Module contenant les vues principales de l'application oc_lettings_site.

Ce module définit la vue principale pour la page d'accueil du site.
"""
import logging
from django.shortcuts import render

logger = logging.getLogger('oc_lettings_site')


def home(request):
    """
    Vue pour la page d'accueil du site.

    Args:
        request: L'objet HttpRequest de Django.

    Returns:
        HttpResponse: La réponse HTTP avec le template rendu.
    """
    logger.info(f"Page d'accueil visitée par {request.META.get('REMOTE_ADDR', 'IP inconnue')}")

    try:
        return render(request, 'oc_lettings_site/index.html')
    except Exception as e:
        logger.error(f"Erreur lors du rendu de la page d'accueil: {str(e)}")
        raise

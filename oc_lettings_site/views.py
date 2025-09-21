"""
Module contenant les vues principales de l'application oc_lettings_site.

Ce module définit la vue principale pour la page d'accueil du site.
"""
import logging
from django.shortcuts import render

logger = logging.getLogger('oc_lettings_site')


def home(request):
    """
    Vue pour la page d'accueil du site Orange County Lettings.

    Cette vue affiche la page d'accueil principale avec les liens vers les sections
    lettings et profiles. Enregistre automatiquement les visites pour le monitoring.

    Args:
        request (HttpRequest): L'objet HttpRequest de Django contenant les métadonnées
                              de la requête (headers, IP, session, etc.)

    Returns:
        HttpResponse: Réponse HTTP avec le template 'oc_lettings_site/index.html' rendu
                     contenant les liens de navigation principaux

    Raises:
        Exception: Re-lance toute exception survenue pendant le rendu après logging
                  (erreurs de template, problèmes de contexte, etc.)

    Side Effects:
        - Enregistre un log INFO avec l'adresse IP du visiteur
        - En cas d'erreur : enregistre un log ERROR avant de re-lancer l'exception

    Template:
        oc_lettings_site/index.html : Page d'accueil avec navigation

    URL Pattern:
        '' (racine) : Accessible via l'URL racine du site

    Example:
        GET / HTTP/1.1
        -> Affiche la page d'accueil avec liens vers /lettings/ et /profiles/
    """
    logger.info(f"Page d'accueil visitée par {request.META.get('REMOTE_ADDR', 'IP inconnue')}")

    try:
        return render(request, 'oc_lettings_site/index.html')
    except Exception as e:
        logger.error(f"Erreur lors du rendu de la page d'accueil: {str(e)}")
        raise

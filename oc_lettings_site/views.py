"""
Module contenant les vues principales de l'application oc_lettings_site.

Ce module définit la vue principale pour la page d'accueil du site.
"""
from django.shortcuts import render


def home(request):
    """
    Vue pour la page d'accueil du site.

    Args:
        request: L'objet HttpRequest de Django.

    Returns:
        HttpResponse: La réponse HTTP avec le template rendu.
    """
    return render(request, 'oc_lettings_site/index.html')

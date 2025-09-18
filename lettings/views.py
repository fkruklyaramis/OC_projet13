"""
Module contenant les vues pour l'application lettings.

Ce module définit les vues pour afficher la liste des locations
et les détails d'une location spécifique.
"""
from django.shortcuts import render, get_object_or_404
from .models import Letting


def index(request):
    """
    Affiche la liste des locations.

    Args:
        request: L'objet HttpRequest de Django.

    Returns:
        HttpResponse: La réponse HTTP avec le template rendu.
    """
    lettings_list = Letting.objects.all()
    context = {'lettings_list': lettings_list}
    return render(request, 'lettings/index.html', context)


def letting(request, letting_id):
    """
    Affiche les détails d'une location spécifique.

    Args:
        request: L'objet HttpRequest de Django.
        letting_id: L'identifiant de la location à afficher.

    Returns:
        HttpResponse: La réponse HTTP avec le template rendu.
    """
    letting = get_object_or_404(Letting, id=letting_id)
    context = {
        'title': letting.title,
        'address': letting.address,
    }
    return render(request, 'lettings/letting.html', context)

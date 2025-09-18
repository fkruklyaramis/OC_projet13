"""
Module contenant les vues pour l'application profiles.

Ce module définit les vues pour afficher la liste des profils
et les détails d'un profil spécifique.
"""
from django.shortcuts import render, get_object_or_404
from .models import Profile


def index(request):
    """
    Affiche la liste des profils.

    Args:
        request: L'objet HttpRequest de Django.

    Returns:
        HttpResponse: La réponse HTTP avec le template rendu.
    """
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)


def profile(request, username):
    """
    Affiche les détails d'un profil spécifique.

    Args:
        request: L'objet HttpRequest de Django.
        username: Le nom d'utilisateur du profil à afficher.

    Returns:
        HttpResponse: La réponse HTTP avec le template rendu.
    """
    profile = get_object_or_404(Profile, user__username=username)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)

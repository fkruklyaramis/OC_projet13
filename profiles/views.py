from django.shortcuts import render
from .models import Profile


def index(request):
    """
    Affiche la liste des profils.
    """
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    # Utilise le nouveau chemin du template
    return render(request, 'profiles/index.html', context)
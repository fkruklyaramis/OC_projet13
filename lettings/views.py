from django.shortcuts import render
from .models import Letting


def index(request):
    """
    Affiche la liste des locations.
    """
    lettings_list = Letting.objects.all()
    context = {'lettings_list': lettings_list}
    # Utilise le nouveau chemin du template
    return render(request, 'lettings/index.html', context)
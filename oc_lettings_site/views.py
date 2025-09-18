from django.shortcuts import render


def home(request):
    """
    Vue pour la page d'accueil du site.
    """
    return render(request, 'oc_lettings_site/index.html')

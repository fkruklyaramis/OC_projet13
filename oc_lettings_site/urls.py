"""
Configuration principale des URLs du projet oc_lettings_site.

Ce module définit les patterns d'URLs racines du projet
et inclut les URLs des applications lettings et profiles.
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Page d'accueil
    path('lettings/', include('lettings.urls', namespace='lettings')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
]

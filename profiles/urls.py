"""
Configuration des URLs pour l'application profiles.

Ce module définit les patterns d'URLs pour accéder aux vues
de l'application profiles.
"""
from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.profile, name='profile'),
]

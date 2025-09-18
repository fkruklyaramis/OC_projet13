"""
Configuration des URLs pour l'application lettings.

Ce module définit les patterns d'URLs pour accéder aux vues
de l'application lettings.
"""
from django.urls import path
from . import views

app_name = 'lettings'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:letting_id>/', views.letting, name='letting'),
]

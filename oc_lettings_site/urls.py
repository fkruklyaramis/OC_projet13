"""
Configuration principale des URLs du projet oc_lettings_site.

Ce module définit les patterns d'URLs racines du projet
et inclut les URLs des applications lettings et profiles.
Configure également les handlers d'erreurs personnalisés.
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Page d'accueil
    path('lettings/', include('lettings.urls', namespace='lettings')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    # URLs de test Sentry (DEBUG uniquement)
    path('test-404/', views.test_sentry_404, name='test_404'),
    path('test-500/', views.test_sentry_500, name='test_500'),
    path('test-sentry/', views.test_sentry_manual, name='test_sentry'),
]

# Configuration des handlers d'erreurs personnalisés avec Sentry
handler404 = 'oc_lettings_site.views.handler404'
handler500 = 'oc_lettings_site.views.handler500'

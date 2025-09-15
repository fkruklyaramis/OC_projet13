from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.index, name='index'),
    # Ajoute ici les autres vues de profiles si besoin
]
from django.urls import path
from . import views

app_name = 'lettings'

urlpatterns = [
    path('', views.index, name='index'),
    # Ajoute ici les autres vues de lettings si besoin
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lettings/', include('lettings.urls', namespace='lettings')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('', include('lettings.urls', namespace='lettings')),  # Ajoute cette ligne pour que la racine affiche lettings
]
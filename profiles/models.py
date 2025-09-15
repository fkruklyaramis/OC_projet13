from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Modèle représentant un profil utilisateur.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """
        Retourne le nom d'utilisateur du profil.
        """
        return self.user.username
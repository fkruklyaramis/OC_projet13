from django.db import models


class Address(models.Model):
    """
    Modèle représentant une adresse.
    """
    number = models.PositiveIntegerField(null=False)
    street = models.CharField(max_length=64, null=False)
    city = models.CharField(max_length=64, null=False)
    state = models.CharField(max_length=2, null=False)
    zip_code = models.PositiveIntegerField(null=False)
    country_iso_code = models.CharField(max_length=3, null=False)

    def __str__(self):
        """
        Retourne une représentation textuelle de l'adresse.
        """
        return f'{self.number} {self.street}, {self.city}'


class Letting(models.Model):
    """
    Modèle représentant une location.
    """
    title = models.CharField(max_length=256, null=False)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        """
        Retourne le titre de la location.
        """
        return self.title
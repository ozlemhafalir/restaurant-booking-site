from django.db import models


class Cuisine(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

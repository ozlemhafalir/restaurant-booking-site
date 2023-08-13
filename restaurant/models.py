from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models
from management.models import City, Cuisine


class Restaurant(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        APPROVED = 'approved'
        ACTIVE = 'active'

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    address = models.CharField(max_length=500, )
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    cuisines = models.ManyToManyField(Cuisine, related_name='restaurants')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurants')
    menu = CloudinaryField('image', default='placeholder')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def cuisine_names(self):
        return ", ".join([cuisine.name for cuisine in self.cuisines.all()])

    def __str__(self):
        return self.name


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', default='placeholder')

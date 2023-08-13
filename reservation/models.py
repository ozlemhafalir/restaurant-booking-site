from django.db import models
from django.conf import settings
from restaurant.models import Restaurant


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        APPROVED = 'approved'
        DECLINED = 'declined'
        CANCELLED = 'cancelled'

    date = models.DateField()
    guests = models.IntegerField()
    note = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date', '-created_on')

    def __str__(self):
        return f'{self.restaurant.name} - {self.date.strftime("%m/%d/%Y")} - {self.guests}'
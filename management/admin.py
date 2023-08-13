from django.contrib import admin
from management.models import City, Cuisine


# Register your models here.

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    pass
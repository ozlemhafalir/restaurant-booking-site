from django.contrib import admin

from restaurant.models import Restaurant, RestaurantImage


class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'created_on')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('status', 'created_on')
    inlines = (RestaurantImageInline,)
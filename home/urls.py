from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('account/reservations/', views.AccountReservationsView.as_view(), name='account_reservations'),
    path('account/restaurants/', views.AccountRestaurantsView.as_view(), name='account_restaurants'),
    path('account/restaurant/<id>/reservations/', views.AccountRestaurantReservationsView.as_view(),
         name='account_restaurant_reservations'),
    path('account/restaurant/<id>/detail/', views.AccountRestaurantDetail.as_view(),
         name='account_restaurant_detail'),
    path('account/restaurant/<restaurant_id>/photos/', views.AccountRestaurantPhotos.as_view(),
         name='account_restaurant_photos'),
    path('account/restaurant/<restaurant_id>/photos/create/', views.AccountRestaurantPhotosCreateView.as_view(),
         name='account_restaurant_photos_create'),
    path('account/restaurant/<restaurant_id>/photos/delete/<pk>/', views.AccountRestaurantPhotosDeleteView.as_view(),
         name='account_restaurant_photos_delete'),
    path('account/profile/', views.AccountProfileView.as_view(), name='account_profile'),
]
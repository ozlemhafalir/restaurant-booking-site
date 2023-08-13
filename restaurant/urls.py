from . import views
from django.urls import path


urlpatterns = [
    path('', views.RestaurantList.as_view(), name='restaurants'),
    path('register/', views.RegisterRestaurant.as_view(), name='register_restaurant'),
    path('register/form/', views.RestaurantRegistrationFormView.as_view(), name='register_restaurant_form'),
    path('register/thanks/', views.RegisterRestaurantThanksView.as_view(), name='register_restaurant_thanks'),
    path('<slug:slug>/', views.RestaurantDetail.as_view(), name='restaurant_detail'),
]
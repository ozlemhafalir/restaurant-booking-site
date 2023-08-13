from . import views
from django.urls import path


urlpatterns = [
    path('form/', views.ReservationFormView.as_view(), name='reservation_form'),
    path('thanks/', views.ThanksView.as_view(), name='reservation_thanks'),
    path('reservation/<int:id>/<action>', views.ReservationActionView.as_view(), name='reservation_action'),
]
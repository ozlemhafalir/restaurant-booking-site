from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views import generic, View
from django import forms

from reservation.models import Reservation
from restaurant.models import Restaurant
from django.utils import timezone


class ReservationForm(forms.Form):
    date = forms.DateField(required=True)
    guests = forms.IntegerField(required=True)
    note = forms.CharField(max_length=1000)
    restaurant_id = forms.IntegerField(required=True)

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise forms.ValidationError('the date must be after now.')
        return date

    def save(self, user):
        restaurant = Restaurant.objects.get(pk=self.cleaned_data.get('restaurant_id'))
        reservation = Reservation.objects.create(
            date=self.cleaned_data.get('date'),
            guests=self.cleaned_data.get('guests'),
            note=self.cleaned_data.get('note'),
            restaurant=restaurant,
            user=user
        )


class ReservationFormView(generic.FormView):
    template_name = "components/reservation-form.html"
    form_class = ReservationForm
    success_url = "/reservation/thanks/"

    def form_valid(self, form):
        form.save(self.request.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ThanksView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'reservation-result.html',
        )


class ReservationActionView(View):
    def post(self, request, id, action, *args, **kwargs):
        user = self.request.user
        reservation = Reservation.objects.get(pk=id)
        if action == 'approve' or action == 'decline':
            if reservation.restaurant.owner != user:
                raise PermissionDenied()
            else:
                if action == 'approve':
                    reservation.status = Reservation.Status.APPROVED
                elif action == 'decline':
                    reservation.status = Reservation.Status.DECLINED
        if action == 'cancel':
            if reservation.user != user:
                raise PermissionDenied()
            else:
                reservation.status = Reservation.Status.CANCELLED
        reservation.save()
        redirect_url = request.GET.get('next')
        if redirect_url:
            return redirect(redirect_url)
        return redirect('home')

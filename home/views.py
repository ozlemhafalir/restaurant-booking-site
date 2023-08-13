import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views import generic

from management.models import City, Cuisine
from reservation.models import Reservation
from restaurant.models import Restaurant, RestaurantImage


# Create your views here.
class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_restaurants"] = Restaurant.objects.all()[:4]
        context["recently_added_restaurants"] = Restaurant.objects.order_by('-created_on').all()[:4]
        context["cities"] = City.objects.all()
        context["cuisines"] = Cuisine.objects.all()

        return context


class AccountProfileView(View):
    template_name = "account-profile.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        return render(request, self.template_name, {"user": user})

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user.first_name = self.request.POST.get('first_name')
        user.last_name = self.request.POST.get('last_name')
        user.email = self.request.POST.get('email')
        user.save()
        return render(request, self.template_name, {"user": user})


class AccountReservationsView(generic.TemplateView):
    template_name = "account-reservations.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context["upcoming"] = Reservation.objects.filter(user=user, date__gte=datetime.datetime.now()).order_by('-date',
                                                                                                                '-created_on')
        context["past"] = Reservation.objects.filter(user=user, date__lte=datetime.datetime.now()).order_by('-date',
                                                                                                            '-created_on')
        return context


class AccountRestaurantsView(generic.TemplateView):
    template_name = "account-restaurants.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        print('user_restaurants')
        print(user.restaurants.all())
        print('restaurant_owned_by_user')
        print(Restaurant.objects.filter(owner=user).all())
        return context


class AccountRestaurantReservationsView(View):
    def get(self, request, id, *args, **kwargs):
        user = self.request.user
        restaurant = Restaurant.objects.get(id=id, owner=user)
        date = self.request.GET.get('date')
        page = self.request.GET.get('page')
        reservations = Reservation.objects.filter(restaurant=restaurant)
        if date:
            reservations = reservations.filter(date=date)
        else:
            reservations = reservations.filter(date__gte=datetime.datetime.now())
        reservations = reservations.order_by('-date')
        reservations_paginator = Paginator(reservations, 20)
        if page:
            reservations = reservations_paginator.get_page(page)
        else:
            reservations = reservations_paginator.get_page(1)
        context = {
            'restaurant': restaurant,
            'reservations': reservations,
            'date': date if date else ''
        }
        return render(request, 'account-restaurant-reservations.html', context)


class AccountRestaurantDetail(View):
    def get(self, request, id, *args, **kwargs):
        user = self.request.user
        restaurant = Restaurant.objects.get(id=id, owner=user)
        context = {
            'restaurant': restaurant,
            'reservations': Reservation.objects.filter(restaurant=restaurant).order_by('-date'),
            "cities": City.objects.all(),
            "cuisines": Cuisine.objects.all()
        }
        return render(request, 'account-restaurant-detail.html', context)

    def post(self, request, id, *args, **kwargs):
        user = self.request.user
        restaurant = Restaurant.objects.get(id=id, owner=user)
        restaurant.name = self.request.POST.get('name')
        restaurant.address = self.request.POST.get('address')
        restaurant.city = City.objects.get(id=self.request.POST.get('city'))
        if self.request.FILES.get('menu'):
            restaurant.menu = self.request.FILES.get('menu')
        cuisines = self.request.POST.getlist('cuisines')
        restaurant.cuisines.clear()
        for cuisine in cuisines:
            restaurant.cuisines.add(Cuisine.objects.get(id=cuisine))
        restaurant.save()
        context = {
            'restaurant': restaurant,
            'reservations': Reservation.objects.filter(restaurant=restaurant).order_by('-date'),
            "cities": City.objects.all(),
            "cuisines": Cuisine.objects.all()
        }
        return render(request, 'account-restaurant-detail.html', context)


class AccountRestaurantPhotos(generic.ListView):
    template_name = "account-restaurant-photos.html"

    def get_queryset(self, *args, **kwargs):
        return RestaurantImage.objects.filter(restaurant=self.kwargs['restaurant_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        print(context)
        return context


class AccountRestaurantPhotosCreateView(generic.CreateView):
    model = RestaurantImage
    fields = ['image']

    def form_valid(self, form):
        form.instance.restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('account_restaurant_photos', kwargs={'restaurant_id': self.kwargs['restaurant_id']})


class AccountRestaurantPhotosDeleteView(generic.DeleteView):
    model = RestaurantImage

    def get_success_url(self):
        return reverse('account_restaurant_photos', kwargs={'restaurant_id': self.kwargs['restaurant_id']})
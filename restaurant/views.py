import uuid

from django.conf import settings
from django import forms
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views import generic, View

from management.models import City, Cuisine
from restaurant.models import Restaurant
from restaurant_booking import settings


class RestaurantList(generic.ListView):
    model = Restaurant
    template_name = 'restaurant-search.html'
    paginate_by = 10

    @property
    def selected_city(self):
        query_string = self.request.GET
        selected_city = query_string.get("city")
        return selected_city

    @property
    def selected_cuisine(self):
        query_string = self.request.GET
        selected_city = query_string.get("cuisine")
        return selected_city

    def get_queryset(self):
        queryset = Restaurant.objects.filter(status=Restaurant.Status.ACTIVE)
        if self.selected_city != 'all':
            queryset = queryset.filter(city__name=self.selected_city)
        if self.selected_cuisine != 'all':
            queryset = queryset.filter(cuisines__name=self.selected_cuisine)
        queryset = queryset.order_by('-created_on')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cities"] = City.objects.all()
        context["cuisines"] = Cuisine.objects.all()
        context["selected_city"] = self.selected_city
        context["selected_cuisine"] = self.selected_cuisine

        return context


class RestaurantDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Restaurant.objects.filter(status=Restaurant.Status.ACTIVE)
        restaurant = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            'restaurant-detail.html',
            {
                'restaurant': restaurant,
                'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
            }
        )


class RegisterRestaurant(View):

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'register-restaurant.html',
            {
                "cities": City.objects.all(),
                "cuisines": Cuisine.objects.all()
            }
        )


class RestaurantRegistrationForm(forms.Form):
    name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    description = forms.CharField(required=True)
    city = forms.IntegerField(required=True)
    # cuisines = forms.MultipleChoiceField(required=False)

    def save(self, user):
        print("save")
        print(self.cleaned_data.get('name'))
        print(self.cleaned_data.get('address'))
        print(self.cleaned_data.get('description'))
        print(self.cleaned_data.get('city'))
        Restaurant.objects.create(
            name=self.cleaned_data.get('name'),
            address=self.cleaned_data.get('address'),
            description=self.cleaned_data.get('description'),
            city=City.objects.get(pk=self.cleaned_data.get('city')),
            slug=slugify(self.cleaned_data.get('name')+str(uuid.uuid4())[:8]),
            owner=user
        )


class RestaurantRegistrationFormView(generic.FormView):
    template_name = "components/restaurant-registration-form.html"
    form_class = RestaurantRegistrationForm
    success_url = "/restaurant/register/thanks/"

    def form_valid(self, form):
        form.save(self.request.user)
        return super().form_valid(form)


class RegisterRestaurantThanksView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'restaurant-registration-result.html',
        )
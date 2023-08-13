from django.views import generic

from management.models import City, Cuisine
from restaurant.models import Restaurant


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

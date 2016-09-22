from django.views.generic import DetailView, ListView

from .models import Event

class HomeView(ListView):
    model = Event
    template_name = 'index.html'

class EventView(DetailView):
    model = Event
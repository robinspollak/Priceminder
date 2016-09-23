from django.views.generic import DetailView, ListView

from .models import Event

class HomeView(ListView):
    model = Event
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['not_on_sale'] = self.not_on_sale()
        return context

    def not_on_sale(self):
        upcoming = ['Lollapalooza', 'Bonnaroo', "Governor's Ball", "EDC: Las Vegas", "South by Southwest"]
        return upcoming

class EventView(DetailView):
    model = Event
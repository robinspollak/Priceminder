from django.views.generic import DetailView, ListView

from pricetracker.settings import trim_datetime

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

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        self.prepare_chart_data()
        return context

    def prepare_chart_data(self):
        sections = self.object.sections.all()
        prepared_data = []
        data_labels = ['Date']
        dates = []
        for section in sections:
            data_labels.append(section.name)
            for pricepoint in section.pricepoints.all().order_by('datetime'):
                dt = pricepoint.datetime.strftime("%m/%d/%Y, %I:%M%p")
                if dt not in dates:
                    dates.append(dt)
        prepared_data.append(data_labels)
        dates = sorted([[date] for date in dates])
        for section in sections:
            pricepoints = list(section.pricepoints.all().order_by('datetime'))
            for i in range(len(pricepoints)):
                dates[i].append(pricepoints[i].total_amount)
        for date in dates:
            prepared_data.append(date)
        return prepared_data
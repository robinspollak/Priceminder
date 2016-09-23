from django.views.generic import DetailView, ListView

from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart

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
        context['section_names'] = map(lambda section: section.name.replace(" ", "_").replace("-",""),
                                       list(self.object.sections.all()))
        context['charts'] = self.create_charts()
        return context

    def create_charts(self):
        charts = {}
        for section in self.object.sections.all():
            data = self.prepare_chart_data(section)
            # data_source = SimpleDataSource(data=data)
            # chart = LineChart(data_source)
            charts[section.name.replace(" ", "_").replace("-","")] = data
        return charts

    def prepare_chart_data(self, section):
        prepared_data = [['Date', 'Price']]
        for pricepoint in section.pricepoints.all().order_by('datetime'):
            data_point = [trim_datetime(pricepoint.datetime),\
                          pricepoint.total_amount]
            prepared_data.append(data_point)
        return prepared_data
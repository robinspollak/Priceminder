from django.views.generic import DetailView, ListView

import requests

from pricetracker.core import trim_datetime, get_secret
from pricepoint.models import Pricepoint
from .models import Event, Section

class HomeView(ListView):
    model = Event
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['not_on_sale'] = self.not_on_sale()
        return context

    def not_on_sale(self):
        upcoming = sorted(['Lollapalooza', 'Bonnaroo', "Governor's Ball", "EDC: Las Vegas", "South by Southwest"])
        return upcoming

    def get_queryset(self):
        return Event.objects.all().order_by('name')

class EventView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        context['section_names'] = map(lambda section: (section.name.replace(" ", "_").replace("-",""), section.id),
                                       list(self.object.sections.all()))
        context['charts'] = self.create_charts()
        return context

    def create_charts(self):
        charts = {}
        for section in self.object.sections.all():
            data = self.prepare_chart_data(section)
            charts[section.name.replace(" ", "_").replace("-","")] = data
        return charts

    def prepare_chart_data(self, section):
        prepared_data = []
        for pricepoint in section.pricepoints.all().order_by('datetime'):
            data_point = [trim_datetime(pricepoint.datetime),\
                          pricepoint.total_amount]
            prepared_data.append(data_point)
        return prepared_data

class SectionView(DetailView):
    model = Section

    def get_context_data(self, **kwargs):
        context = super(SectionView, self).get_context_data(**kwargs)
        context['current_cheapest'] = self.price_if_necessary()
        context['cheapest_ever'] = self.object.pricepoints.all().order_by('total_amount', '-id').first()
        context['chart'] = self.prepare_chart_data()
        return context

    def prepare_chart_data(self):
        prepared_data = []
        for pricepoint in self.object.pricepoints.all().order_by('datetime'):
            data_point = [trim_datetime(pricepoint.datetime),\
                          pricepoint.total_amount]
            prepared_data.append(data_point)
        return prepared_data

    def price_if_necessary(self):
        # Check if price is now cheaper
        response = self.object.retrieve_pricepoint()
        current_cheapest = self.object.pricepoints.last()
        retrieved_cheapest = response['listing'][0]
        new_different = (retrieved_cheapest['currentPrice']['amount'] != current_cheapest.total_amount)
        # Check if old cheapest price is expired
        if not new_different:
            listing_url = get_secret('STUBHUB_LISTING_URL') + current_cheapest.listing_id
            headers = get_secret('STUBHUB_POST_HEADER')
            listing_response = requests.get(listing_url, headers=headers, params={}).json()
            cheapest_expired = 'errors' in listing_response['ListingResponse']
        if new_different or cheapest_expired:
            pricepoint = self.object.create_pricepoint(response)
            if pricepoint.total_amount == current_cheapest.total_amount:
                current_cheapest.delete()
        else:
            pricepoint = current_cheapest
        return pricepoint

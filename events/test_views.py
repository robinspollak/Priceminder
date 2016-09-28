from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse

from pricetracker.tests import setup_view
from pricetracker.core import trim_datetime
from .models import Event, Section
from .views import *

class HomeViewTestCase(TestCase):
    def setUp(self):
        self.event1 = Event.objects.create(name='a test', stubhub_id='9599084')
        self.event2 = Event.objects.create(name='b test', stubhub_id='9569783')
        self.url = reverse('events:home')
        self.request = RequestFactory().get(self.url)
        self.view = setup_view(HomeView(),
                               self.request)
        self.view.object_list = None

    def test_not_on_sale(self):
        not_on_sale = sorted(['Lollapalooza', 'Bonnaroo', "Governor's Ball", "EDC: Las Vegas", "South by Southwest"])
        self.assertEquals(not_on_sale, self.view.not_on_sale())

    def test_get_queryset(self):
        events = list(Event.objects.all().order_by('name'))
        queryset = list(self.view.get_queryset())
        self.assertEquals(events, queryset)

    def test_get_context_data(self):
        context = self.view.get_context_data()
        self.assertEquals(self.view.not_on_sale(),
                          context['not_on_sale'])


class EventViewTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(name='test Event', stubhub_id='9599084')
        self.section1 = Section.objects.create(name='test Section 1', stubhub_id='592806', event=self.event)
        self.section2 = Section.objects.create(name='test Section 2', stubhub_id='592807', event=self.event)
        self.pricepoint1 = Pricepoint.objects.create(raw_amount=123.45,
                                                    total_amount=234.56,
                                                    listing_id='123456',
                                                    section = self.section1)
        self.pricepoint2 = Pricepoint.objects.create(raw_amount=234.56,
                                                    total_amount=345.67,
                                                    listing_id='654321',
                                                    section = self.section1)
        self.url = reverse('events:event',
                           kwargs={'pk': self.event.id})
        self.request = RequestFactory().get(self.url)
        self.view = setup_view(EventView(),
                               self.event.id,
                               self.request)
        self.view.object = self.event

    def test_create_charts(self):
        charts = {}
        for section in self.event.sections.all():
            data = self.view.prepare_chart_data(section)
            charts[section.name.replace(" ", "_").replace("-","")] = data
        self.assertEquals(charts, self.view.create_charts())

    def test_prepare_chart_data(self):
        prepared_data = []
        for pricepoint in self.section1.pricepoints.all().order_by('datetime'):
            data_point = [trim_datetime(pricepoint.datetime),\
                          pricepoint.total_amount]
            prepared_data.append(data_point)
        self.assertEquals(prepared_data, self.view.prepare_chart_data(self.section1))

    def test_get_context_data(self):
        context = self.view.get_context_data()
        result = map(lambda section: (section.name.replace(" ", "_").replace("-",""), section.id),
                     list(self.event.sections.all()))
        self.assertEquals(result, context['section_names'])
        charts = self.view.create_charts()
        self.assertEquals(charts, context['charts'])


class SectionViewTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(name='test Event', stubhub_id='9599084')
        self.section = Section.objects.create(name='test Section 1', stubhub_id='592806', event=self.event)
        self.pricepoint1 = Pricepoint.objects.create(raw_amount=123.45,
                                                     total_amount=234.56,
                                                     listing_id=123456,
                                                     section = self.section)
        self.pricepoint2 = Pricepoint.objects.create(raw_amount=234.56,
                                                     total_amount=345.67,
                                                     listing_id=654321,
                                                     section = self.section)
        self.url = reverse('events:section',
                           kwargs={'event_id': self.event.id,
                                   'pk': self.section.id})
        self.request = RequestFactory().get(self.url)
        self.view = setup_view(SectionView(),
                               self.event.id,
                               self.section.id,
                               self.request)
        self.view.object = self.section

    def test_price_if_necessary_different_price(self):
        response = self.view.object.retrieve_pricepoint()
        current_cheapest = self.view.object.pricepoints.last()
        result = self.view.price_if_necessary()
        pricepoint = self.view.object.create_pricepoint(response)
        self.assertEquals(pricepoint.raw_amount, result.raw_amount)
        self.assertEquals(pricepoint.total_amount, result.total_amount)
        self.assertEquals(pricepoint.listing_id, result.listing_id)
        self.assertEquals(pricepoint.section, result.section)

    def test_price_if_necessary_listing_expired(self):
        response = self.view.object.retrieve_pricepoint()
        pricepoint = self.view.object.create_pricepoint(response)
        pricepoint.stubhub_id = '123'
        pricepoint.save()
        result = self.view.price_if_necessary()
        self.assertEquals(pricepoint.raw_amount, result.raw_amount)
        self.assertEquals(pricepoint.total_amount, result.total_amount)
        self.assertEquals(pricepoint.listing_id, result.listing_id)
        self.assertEquals(pricepoint.section, result.section)

    def test_price_if_necessary_unecessary(self):
        response = self.view.object.retrieve_pricepoint()
        pricepoint = self.view.object.create_pricepoint(response)
        result = self.view.price_if_necessary()
        self.assertEquals(pricepoint, result)

    def test_prepare_chart_data(self):
        prepared_data = []
        for pricepoint in self.section.pricepoints.all().order_by('datetime'):
            data_point = [trim_datetime(pricepoint.datetime),\
                          pricepoint.total_amount]
            prepared_data.append(data_point)
        self.assertEquals(prepared_data, self.view.prepare_chart_data())

    def test_get_context_data(self):
        context = self.view.get_context_data()
        self.assertEquals(self.view.prepare_chart_data(), context['chart'])
        self.assertEquals(self.pricepoint1, context['cheapest_ever'])


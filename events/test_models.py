from django.test import TestCase

from pricetracker.core import get_secret
from .models import *

class EventTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(name='test', stubhub_id='9599084')

    def test___unicode__(self):
        self.assertEquals(self.event.name, self.event.__unicode__())


class SectionTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(name='test Event', stubhub_id='9599084')
        self.section = Section.objects.create(name='test Section', stubhub_id='592806', event=self.event)
        self.inventory_url = get_secret('STUBHUB_API_URL')
        self.headers = get_secret('STUBHUB_POST_HEADER')

    def test___unicode__(self):
        result = self.section.name + " at " + self.section.event.name
        self.assertEquals(result, self.section.__unicode__())

    def test_retrieve_pricepoint_multple_sections(self):
        '''test retrieve pricepoint on an event with multiple sections'''
        query_data = {
            'eventid': self.section.event.stubhub_id,
            'sectionidlist': [self.section.stubhub_id],
            'rows': 1
            }
        response = requests.get(self.inventory_url, headers=self.headers, params=query_data).json()
        self.assertEquals(response, self.section.retrieve_pricepoint())

    def test_retrieve_pricepoint_one_section(self):
        '''test retrieve pricepoint on an event with one section'''
        event = Event.objects.create(name='test Event', stubhub_id='9569783')
        section = Section.objects.create(name='test Section 2', event=event)
        query_data = {
            'eventid': section.event.stubhub_id,
            'rows': 1
            }        
        response = requests.get(self.inventory_url, headers=self.headers, params=query_data).json()
        self.assertEquals(response, section.retrieve_pricepoint())        

    def test_create_pricepoint_with_tickets(self):
        response = self.section.retrieve_pricepoint()
        cheapest_ticket = response['listing'][0]
        result = self.section.create_pricepoint(response)
        self.assertEquals(cheapest_ticket['listingPrice']['amount'], result.raw_amount)
        self.assertEquals(cheapest_ticket['currentPrice']['amount'], result.total_amount)
        self.assertEquals(unicode(cheapest_ticket['listingId']), result.listing_id)
        self.assertEquals(self.section, result.section)

    def test_create_pricepoint_with_no_tickets(self):
        section = Section.objects.create(name='test Section no tickets', stubhub_id='123456', event=self.event)
        response = self.section.retrieve_pricepoint
        result = self.section.create_pricepoint(response)
        self.assertEquals(0.0, result.raw_amount)
        self.assertEquals(0.0, result.total_amount)
        self.assertEquals('0', result.listing_id)
        self.assertEquals(self.section, result.section)

    def test_set_pricepoint(self):
        response = self.section.retrieve_pricepoint()
        pricepoint = self.section.create_pricepoint(response)
        result = self.section.set_pricepoint()
        self.assertEquals(pricepoint.raw_amount, result.raw_amount)
        self.assertEquals(pricepoint.total_amount, result.total_amount)
        self.assertEquals(pricepoint.listing_id, result.listing_id)
        self.assertEquals(pricepoint.section, result.section)
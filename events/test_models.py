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

    def test___unicode__(self):
        result = self.section.name + " at " + self.section.event.name
        self.assertEquals(result, self.section.__unicode__())

    def test_set_pricepoint(self):
        '''not sure how to test this guy fully'''
        pricepoint = self.section.set_pricepoint()
        self.assert_(True)
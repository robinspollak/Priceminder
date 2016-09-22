from django.test import TestCase

from datetime import datetime

from events.models import Event, Section
from .models import Pricepoint

class PricepointTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(name='test Event', stubhub_id='1234')
        self.section = Section.objects.create(name='test Section', stubhub_id='12345', event=self.event)
        self.now = datetime.now()
        self.pricepoint = Pricepoint.objects.create(raw_amount=123.45,
                                                    total_amount=234.56,
                                                    section = self.section)

    def test___unicode__(self):
        now = self.pricepoint.datetime
        result = self.section.name + " at " + self.section.event.name +\
                   " cost " + unicode(234.56) + " on " + unicode(now)
        self.assertEquals(result, self.pricepoint.__unicode__())


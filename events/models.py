from __future__ import unicode_literals
import json
import requests

from django.db import models

from pricepoint.models import Pricepoint
from pricetracker.settings import get_secret

class Event(models.Model):
    name = models.CharField(max_length=255)
    stubhub_id = models.IntegerField()

    def __unicode__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=255)
    stubhub_id = models.IntegerField()
    event = models.ForeignKey(Event, related_name='sections')

    def __unicode__(self):
        return self.name + " at " + self.event.name

    def set_pricepoint(self):
        inventory_url = 'https://api.stubhub.com/search/inventory/v1'
        headers = get_secret('STUBHUB_POST_HEADER')
        query_data = {
                    'eventid': self.event.stubhub_id,
                    'sectionidlist': [self.stubhub_id],
                    'rows': 1
                    }
        response = requests.get(inventory_url, headers=headers, params=query_data).json()
        cheapest_ticket = response['listing'][0]
        pricepoint = Pricepoint.objects.create(raw_amount=cheapest_ticket['listingPrice']['amount'],
                                               total_amount=cheapest_ticket['currentPrice']['amount'],
                                               section=self)
        return pricepoint


from __future__ import unicode_literals
import json
import requests

from django.db import models

from pricepoint.models import Pricepoint
from pricetracker.core import get_secret

class Event(models.Model):
    name = models.CharField(max_length=255)
    stubhub_id = models.IntegerField()

    def __unicode__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=255)
    stubhub_id = models.IntegerField(null=True, blank=True)
    event = models.ForeignKey(Event, related_name='sections')

    def __unicode__(self):
        return self.name + " at " + self.event.name

    def set_pricepoint(self):
        response = self.retrieve_pricepoint()
        pricepoint = self.create_pricepoint(response)
        return pricepoint


    def create_pricepoint(self, response):
        listings = response['listing']
        for listing in listings:
            listing_url = get_secret('STUBHUB_LISTING_URL') + unicode(listing['listingId'])
            response = requests.get(listing_url, headers=get_secret('STUBHUB_POST_HEADER'), params={}).json()
            if 'errors' not in response['ListingResponse']:
                try:
                    pricepoint = Pricepoint.objects.create(raw_amount=listing['listingPrice']['amount'],
                                                           total_amount=listing['currentPrice']['amount'],
                                                           listing_id=unicode(listing['listingId']),
                                                           section=self)
                except:
                    pricepoint = Pricepoint.objects.create(raw_amount=0.0,
                                                           total_amount=0.0,
                                                           listing_id='0',
                                                           section=self)
                return pricepoint
        return None


    def retrieve_pricepoint(self):
        inventory_url = get_secret('STUBHUB_API_URL')
        headers = get_secret('STUBHUB_POST_HEADER')
        if self.stubhub_id:
            query_data = {
                        'eventid': self.event.stubhub_id,
                        'sectionidlist': [self.stubhub_id],
                        'quantity': 1,
                        'rows': 10
                        }
        else:
            query_data = {
                        'eventid': self.event.stubhub_id,
                        'quantity': 1,
                        'rows': 10
                        }
        response = requests.get(inventory_url, headers=headers, params=query_data).json()
        return response


from __future__ import unicode_literals

from django.db import models

class Pricepoint(models.Model):
    raw_amount = models.FloatField()
    total_amount = models.FloatField()
    datetime = models.DateTimeField(auto_now_add=True)
    listing_id = models.CharField(max_length=12)
    section = models.ForeignKey('events.Section', related_name='pricepoints')

    def __unicode__(self):
        return self.section.name + " at " + self.section.event.name +\
               " cost " + unicode(self.total_amount) + " on " + unicode(self.datetime)
from django_cron import CronJobBase, Schedule

from events.models import Event, Section
from pricepoint.models import Pricepoint

class UpdatePricepoints(CronJobBase):
    RUN_EVERY_MINS = 60*6
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    code = 'events.update_pricepoints'

    def do(self):
        sections = Section.objects.all()
        for section in sections:
            pricepoint = section.set_pricepoint()
            print pricepoint
        
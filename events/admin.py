from django.contrib import admin
from .models import *

admin.site.register(Event, admin.ModelAdmin)
admin.site.register(Section, admin.ModelAdmin)
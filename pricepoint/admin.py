from django.contrib import admin

from .models import *

admin.site.register(Pricepoint, admin.ModelAdmin)
# Register your models here.

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'^(?P<pk>\d+)/$', views.EventView.as_view(), name="event"),
]
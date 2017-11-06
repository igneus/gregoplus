from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<score_id>[0-9]+)$', views.detail, name='detail'),
    # browse by categories
    url(r'^incipit$', views.incipit, name='incipit'),
    url(r'^incipit/(?P<incipit>[_A-Z]{1})$', views.incipit_detail, name='incipit_detail'),
    url(r'^usage$', views.usage, name='usage'),
    url(r'^usage/(?P<usage_id>[a-z]+)$', views.usage_detail, name='usage_detail'),
    url(r'^tag$', views.tag, name='tag'),
    url(r'^source$', views.source, name='source'),
]

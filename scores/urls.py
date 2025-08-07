from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<score_id>[0-9]+)$', views.detail, name='detail'),
    re_path(r'^(?P<score_id>[0-9]+)\.gabc$', views.gabc, name='gabc'),
    # browse by categories
    re_path(r'^incipit$', views.incipit, name='incipit'),
    re_path(r'^incipit/(?P<incipit>[_A-Z]{1})$', views.incipit_detail, name='incipit_detail'),
    re_path(r'^usage$', views.usage, name='usage'),
    re_path(r'^usage/(?P<usage_id>[a-z]+)$', views.usage_detail, name='usage_detail'),
    re_path(r'^tag$', views.tag, name='tag'),
    re_path(r'^source$', views.source, name='source'),
    re_path(r'^source/(?P<source_id>[0-9]+)$', views.source_detail, name='source_detail'),
]

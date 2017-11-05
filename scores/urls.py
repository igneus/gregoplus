from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<score_id>[0-9]+)$', views.detail, name='detail'),
    # browse by categories
    url(r'^incipit$', views.incipit, name='incipit'),
    url(r'^usage$', views.usage, name='usage'),
    url(r'^tag$', views.tag, name='tag'),
    url(r'^source$', views.source, name='source'),
]

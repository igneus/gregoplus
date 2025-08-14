from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:score_id>', views.detail, name='detail'),
    path('<int:score_id>.gabc', views.gabc, name='gabc'),
    # browse by categories
    path('incipit', views.incipit, name='incipit'),
    re_path(r'^incipit/(?P<incipit>([A-Z]{1}|no-lyrics|other))$', views.incipit_detail, name='incipit_detail'),
    path('usage', views.usage, name='usage'),
    re_path(r'^usage/(?P<usage_id>[a-z]+)$', views.usage_detail, name='usage_detail'),
    path('tag', views.tag, name='tag'),
    path('tag/<int:tag_id>', views.tag_detail, name='tag_detail'),
    path('source', views.source, name='source'),
    path('source/<int:source_id>', views.source_detail, name='source_detail'),
]

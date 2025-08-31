from django.contrib import admin

from . import models


@admin.register(models.Chant)
class ScoreAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'office_part',
        'mode',
        'incipit',
        'version',
    ]

    search_fields = [
        'incipit',
    ]
    list_filter = [
        'office_part',
        'mode',
    ]


@admin.register(models.Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'year',
        'editor',
    ]


@admin.register(models.ChantSource)
class ChantSourceAdmin(admin.ModelAdmin):
    list_display = [
        'chant__id',
        'chant__incipit',
        'chant__office_part',
        'source__id',
        'source__title',
        'source__year',
        'page',
        'sequence',
    ]

    autocomplete_fields = ['chant']

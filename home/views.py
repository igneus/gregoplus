from django.shortcuts import render

from scores.models import Chant, Source


def index(request):
    return render(request, 'home/index.html', {
        'scores': Chant.objects.order_by('?')[:2],
        'chant_count': Chant.objects.count(),
        'source_count': Source.objects.count(),
    })

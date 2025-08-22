from django.shortcuts import render

from scores.models import Chant


def index(request):
    return render(request, 'home/index.html', {
        'scores': Chant.objects.order_by('?')[:2]
    })

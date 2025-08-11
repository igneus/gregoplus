from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Score, Source
from .gabc import Gabc

def index(request):
    return render(request, 'scores/index.html')

def detail(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    return render(request, 'scores/detail.html', {'score': score})

def gabc(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    return HttpResponse(Gabc(score))

def incipit(request):
    incipits = [chr(i) for i in range(ord('A'), ord('Z'))]
    return render(request, 'scores/incipit.html', {'incipits': incipits})

def incipit_detail(request, incipit):
    if incipit == '_':
        scores = Score.objects.filter(incipit='')
    else:
        scores = Score.objects.filter(incipit__istartswith=incipit)

    return render(request, 'scores/incipit_detail.html', {'scores': scores, 'incipit': incipit})

def usage(request):
    return render(request, 'scores/usage.html', {'types': Score.OFFICE_PART_CHOICES})

def usage_detail(request, usage_id):
    scores = Score.objects.filter(office_part=usage_id)
    if len(scores) == 0:
        raise Http404()
    return render(request, 'scores/usage_detail.html', {
        'scores': scores,
        'title': scores[0].get_office_part_display(),
    })

def tag(request):
    pass

def source(request):
    sources = Source.objects.all()
    return render(request, 'scores/source.html', {'sources': sources})

def source_detail(request, source_id):
    source = get_object_or_404(Source, id=source_id)
    source_chants = source.chantsource_set.all()
    return render(request, 'scores/source_detail.html', {'source': source, 'source_chants': source_chants})

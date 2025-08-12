from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Chant, Source, Tag
from .gabc import Gabc

def index(request):
    return render(request, 'scores/index.html')

def detail(request, score_id):
    score = get_object_or_404(Chant, id=score_id)
    return render(request, 'scores/detail.html', {'score': score})

def gabc(request, score_id):
    score = get_object_or_404(Chant, id=score_id)
    return HttpResponse(Gabc(score))

def incipit(request):
    incipits = [chr(i) for i in range(ord('A'), ord('Z'))]
    return render(request, 'scores/incipit.html', {'incipits': incipits})

def incipit_detail(request, incipit):
    if incipit == '_':
        scores = Chant.objects.filter(incipit='')
    else:
        scores = Chant.objects.filter(incipit__istartswith=incipit)

    return render(request, 'scores/incipit_detail.html', {'scores': scores, 'incipit': incipit})

def usage(request):
    return render(request, 'scores/usage.html', {'types': Chant.OFFICE_PART_CHOICES})

def usage_detail(request, usage_id):
    scores = Chant.objects.filter(office_part=usage_id)
    if len(scores) == 0:
        raise Http404()
    return render(request, 'scores/usage_detail.html', {
        'scores': scores,
        'title': scores[0].get_office_part_display(),
    })

def tag(request):
    tags = Tag.objects.all()
    return render(request, 'scores/tag.html', {'tags': tags})

def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    scores = Chant.objects.filter(tags=tag)
    return render(request, 'scores/tag_detail.html', {
        'tag': tag,
        'scores': scores,
    })

def source(request):
    sources = Source.objects.all()
    return render(request, 'scores/source.html', {'sources': sources})

def source_detail(request, source_id):
    source = get_object_or_404(Source, id=source_id)
    source_chants = source.chantsource_set.all()
    return render(request, 'scores/source_detail.html', {'source': source, 'source_chants': source_chants})

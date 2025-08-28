from django.db.models import Count
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from .models import Chant, Source, Tag, ChantWithSource
from .gabc import Gabc
from .utils import paginate_if_needed

def index(request):
    scores = Chant.objects.all()
    scores, page_obj = paginate_if_needed(scores, request)
    return render(request, 'scores/index.html', {
        'scores': scores,
        'page_obj': page_obj,
    })

def detail(request, score_id, office_part=None, incipit_slug=None):
    score = get_object_or_404(Chant, id=score_id)

    def _normalize_empty(val):
        return None if val in (None, '') else val

    if office_part != _normalize_empty(score.office_part) or incipit_slug != _normalize_empty(score.incipit_slug()):
        return redirect(score.get_absolute_url(), permanent=True)

    return render(request, 'scores/detail.html', {
        'score': score,
        'gabc': Gabc(score),
        'tags': score.tags.all(),
        'chant_sources': score.chant_sources.all(),
    })

def gabc(request, score_id):
    score = get_object_or_404(Chant, id=score_id)
    return HttpResponse(Gabc(score), content_type='text/plain; charset=utf-8')

def incipit(request):
    incipits = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    return render(request, 'scores/incipit.html', {'incipits': incipits})

def incipit_detail(request, incipit):
    if incipit == 'no-lyrics':
        scores = Chant.objects.filter(incipit='')
    elif incipit == 'other':
        scores = Chant.objects.filter(incipit__iregex='^[^a-z]+')
    else:
        scores = Chant.objects.filter(incipit__istartswith=incipit)

    scores, page_obj = paginate_if_needed(scores, request)
    return render(request, 'scores/incipit_detail.html', {
        'scores': scores,
        'incipit': incipit,
        'page_obj': page_obj,
    })

def usage(request):
    return render(request, 'scores/usage.html', {'types': Chant.OFFICE_PART_CHOICES})

def usage_detail(request, usage_id):
    scores = Chant.objects.filter(office_part=usage_id)
    if scores.count() == 0:
        raise Http404()

    scores, page_obj = paginate_if_needed(scores, request)
    return render(request, 'scores/usage_detail.html', {
        'scores': scores,
        'title': scores[0].get_office_part_display() if hasattr(scores, '__iter__') and scores else Chant.objects.filter(office_part=usage_id).first().get_office_part_display(),
        'page_obj': page_obj,
    })

def tag(request):
    tags = Tag.objects.annotate(chant_count=Count('scores')).filter(chant_count__gt=1)
    return render(request, 'scores/tag.html', {'tags': tags})

def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    scores = Chant.objects.filter(tags=tag)
    scores, page_obj = paginate_if_needed(scores, request)
    return render(request, 'scores/tag_detail.html', {
        'tag': tag,
        'scores': scores,
        'page_obj': page_obj,
    })

def source(request):
    sources = Source.objects.all()
    return render(request, 'scores/source.html', {'sources': sources})

def source_detail(request, source_id):
    source = get_object_or_404(Source, id=source_id)
    source_chants = source.chant_sources.all()
    source_chants, page_obj = paginate_if_needed(source_chants, request)
    source_chants = map(ChantWithSource, source_chants)
    return render(request, 'scores/source_detail.html', {
        'source': source,
        'scores': source_chants,
        'page_obj': page_obj,
    })

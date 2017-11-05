from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Score

def index(request):
    return render(request, 'scores/index.html')

def detail(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    return render(request, 'scores/detail.html', {'score': score})

def incipit(request):
    pass

def usage(request):
    return render(request, 'scores/usage.html', {'types': Score.OFFICE_PART_CHOICES})

def usage_detail(request, usage_id):
    scores = Score.objects.filter(office_part=usage_id).order_by('incipit')
    if len(scores) == 0:
        raise Http404()
    return render(request, 'scores/usage_detail.html', {'scores': scores})

def tag(request):
    pass

def source(request):
    pass

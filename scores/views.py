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
    pass

def tag(request):
    pass

def source(request):
    pass

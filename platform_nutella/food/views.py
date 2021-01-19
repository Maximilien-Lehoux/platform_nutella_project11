from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'food/index.html')


def research(request):
    return render(request, 'food/research.html')


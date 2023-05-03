from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import ListView
from django.views import generic
from django.shortcuts import get_object_or_404

# models 안에 있는 Stations (dummy data) 클래스를 가져옴
from .models import Stations

class IndexView(ListView):
    template_name = 'scraper/index.html'
    context_object_name = 'all_stations'

    def get_queryset(self):
        return Stations.objects.all()

def line_details(request, slug):
    obj = Stations.objects.filter(line=slug)
    line_name = slug
    return render(request, 'scraper/line_details.html', {'obj': obj, 'line_name': line_name})
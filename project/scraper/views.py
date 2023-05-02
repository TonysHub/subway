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

class DetailView(generic.DetailView):
    model = Stations
    context_object_name = 'station'
    template_name = 'scraper/details.html'  
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


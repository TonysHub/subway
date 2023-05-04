from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import ListView
from django.views import generic
from django.shortcuts import get_object_or_404

from .models import Stations

class IndexView(ListView):
    template_name = 'scraper/index.html'
    context_object_name = 'all_lines'
    
    def get_queryset(self):
        return Stations.objects.values('line').distinct()




# 추후에 CBV로 변경
def line_details(request, slug):
    obj = Stations.objects.filter(line=slug)
    line_name = slug
    return render(request, 'scraper/line_details.html', {'obj': obj, 'line_name': line_name})

def station_details(request, line, station):
    # line 검색 추가해서, 예를 들어 3호선에서 고속터미널역 클릭시, 7호선 고속터미널 정보는 안나옴
    obj = get_object_or_404(Stations, station=station, line=line)
    return render(request, 'scraper/station_details.html', {'station': obj})

def search_station(request):
    if request.method == "POST":
        query = request.POST["searched"]
        stations = Stations.objects.filter(station=query)
        return render(request, 'scraper/search_station.html', {'stations': stations, 'station_name': query})
    else:
        return render(request, 'scraper/search_station.html', {})
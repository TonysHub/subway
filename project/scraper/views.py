from django.shortcuts import render
from django.views.generic import ListView
from django.views import generic

# models 안에 있는 Stations 클래스를 가져옴
# from .models import Stations


def index(request):
    return render(request, 'scraper/index.html')

# class IndexView(ListView):
#     template_name = 'scraper/index.html'
#     context_object_name = 'all_stations'

#     def get_queryset(self):
#         # 이 부분은 성현님이 데이터셋 추가하면 구현 가능
#         return Stations.objects.all()

def details(request):
    return render(request, 'scraper/details.html')

class DetailView(generic.DetailView):
    model = Stations
    template_name = 'scraper/details.html'

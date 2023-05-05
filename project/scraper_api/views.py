from rest_framework import viewsets
from scraper_api.serializers import *
from scraper.models import *

class StationsViewSet(viewsets.ModelViewSet):
    queryset = Stations.objects.all()
    serializer_class = StationsSerializer
    
    
class DailyTrafficViewSet(viewsets.ModelViewSet):
    queryset = DailyTraffic.objects.all()
    serializer_class = DailyTrafficSerializer
    
class HourlyTrafficViewSet(viewsets.ModelViewSet):
    queryset = HourlyTraffic.objects.all()
    serializer_class = HourlyTrafficSerializer
    
    



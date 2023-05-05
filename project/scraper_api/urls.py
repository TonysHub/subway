from django.urls import include, path
from rest_framework import routers
from scraper_api.views import *



router = routers.DefaultRouter()
router.register(r'station', StationsViewSet)
router.register(r'daily', DailyTrafficViewSet)
router.register(r'hourly', HourlyTrafficViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
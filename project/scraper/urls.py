from django.urls import path
from . import views
app_name = "scraper"

urlpatterns = [
    path('', views.index, name='index'),
    path('<pk>/', views.details, name='details'),
]
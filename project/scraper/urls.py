from django.urls import path
from . import views
app_name = "scraper"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<slug>/', views.line_details, name='line-details')
]
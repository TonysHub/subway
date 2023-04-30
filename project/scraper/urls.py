from django.urls import path
from . import views
app_name = "scraper"

urlpatterns = [
    path('', views.index, name='index'),
    # leads to /scraper/3/
    # by the end of this project, we should label with 
    # path("<int:line_number>/", views.detail, name="detail")
    # and pass in the line number to views.detail to call the corresponding data
    path('/3/', views.line_three, name='line_three'),
]
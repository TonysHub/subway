from django.shortcuts import render

def index(request):
    return render(request, 'scraper/index.html')

def line_three(request):
    return render(request, 'scraper/line_three.html')


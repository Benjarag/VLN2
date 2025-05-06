from django.shortcuts import render

# Create your views here.
# home/views.py
from django.http import HttpResponse

def home_view(request):
    return render(request, 'home/homepage.html')
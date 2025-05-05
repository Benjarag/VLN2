from django.shortcuts import render

# Create your views here.
# home/views.py
from django.http import HttpResponse

def homepage(request):
    return HttpResponse("Welcome to the homepage!")  # Simple response for testing

from django.shortcuts import render

# Create your views here.
# properties/views.py
from django.http import HttpResponse

def property_listings(request):
    return HttpResponse("This is the property listings page")

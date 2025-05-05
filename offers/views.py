from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def offers(request):
    return HttpResponse("This is the offers page")

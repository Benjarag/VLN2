from django.shortcuts import render

# Create your views here.
# accounts/views.py
# accounts/views.py
from django.shortcuts import render
from django.http import HttpResponse

def login_view(request):
    return HttpResponse("This is the login page")

def signup_view(request):
    return HttpResponse("This is the signup page")

def profile_view(request):
    return HttpResponse("This is the profile page")

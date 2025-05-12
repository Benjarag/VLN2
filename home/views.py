from django.shortcuts import render

# Create your views here.
# home/views.py
from django.http import HttpResponse
from properties.forms import PropertyFilterForm

def home_view(request):
    # Create an empty search form instance
    search_form = PropertyFilterForm()
    return render(request, 'home/homepage.html', {'search_form': search_form})
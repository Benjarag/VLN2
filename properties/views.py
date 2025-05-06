from django.shortcuts import render
from data import PROPERTIES  # Assuming you're importing the data

def property_listings(request):
    return render(request, "properties/property_listings.html", {
        "properties": PROPERTIES
    })


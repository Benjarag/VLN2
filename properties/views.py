from django.shortcuts import render, get_object_or_404
# from data import PROPERTIES  # This is commented out since we're using the model now
from .models import Property

def property_listings(request):
    # Get all property objects from the database
    properties = Property.objects.all()
    
    return render(request, "properties/property_listings.html", {
        "properties": properties
    })

def property_details(request, property_id):
    # Get a specific property or return a 404 if not found
    property = get_object_or_404(Property, id=property_id)
    
    return render(request, "properties/property_details.html", {
        "property": property
    })
from django.shortcuts import render, get_object_or_404
from data import PROPERTIES


def property_listings(request):
    return render(request, "properties/property_listings.html", {
        "properties": PROPERTIES
    })

def property_detail(request, property_id):
    return render(request, "properties/property_details.html", {
        "property": PROPERTIES[property_id]
    })
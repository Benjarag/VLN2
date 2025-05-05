from django.shortcuts import render

# Create your views here.
# sellers/views.py
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Seller  # Assuming you have a Seller model


def seller_profile(request, seller_id):
    # Get the seller from the database
    seller = get_object_or_404(Seller, id=seller_id)

    # Return some details about the seller (you can customize this)
    return HttpResponse(f"This is the profile page for seller {seller.name}")

from django.shortcuts import render

# Create your views here.
# sellers/views.py
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# from .models import Seller
# Assuming you have a Seller model


def seller_profile(request, seller_id):
    # Get the seller from the database
    # seller = get_object_or_404(Seller, id=seller_id)
    # there should be seller email, name, phone number, profile picture and link to the profile page

    # Return some details about the seller (you can customize this)
    # {seller.name}")
    return HttpResponse(f"This is the profile page for seller ")

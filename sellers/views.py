from django.shortcuts import render

# sellers/views.py
from django.shortcuts import render, get_object_or_404
from .models import Seller


def seller_profile(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    properties = seller.properties.all()

    return render(request, 'sellers/seller_profile.html', {
        'seller': seller,
        'properties': properties
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Seller


def seller_profile(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    properties = seller.properties.all()

    return render(request, 'sellers/seller_profile.html', {
        'seller': seller,
        'properties': properties
    })
@login_required
def my_listings(request):
    # Check if user is a seller
    if not hasattr(request.user, 'profile') or not request.user.profile.is_seller:
        messages.error(request, "You don't have seller privileges.")
        return redirect('home')

    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        # Create a basic seller profile if one doesn't exist
        seller = Seller.objects.create(
            user=request.user,
            name=request.user.username,
            email=request.user.email
        )
        messages.warning(request, "Your seller profile has been automatically created.")

    # Get all properties for this seller
    from properties.models import Property
    properties = Property.objects.filter(seller=seller)

    # This is the same template used in seller_profile, but with is_owner=True
    return render(request, 'sellers/seller_profile.html', {
        'seller': seller,
        'properties': properties,
        'is_owner': True  # This flag lets the template know the user owns these listings
    })

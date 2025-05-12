from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Property
from .forms import PropertyFilterForm
from offers.models import PurchaseOffer
from offers.forms import PurchaseOfferForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def property_listings(request):
    # Initialize queryset with all available properties
    properties = Property.objects.all()
    
    filter_form = PropertyFilterForm(request.GET or None)

    # Apply filters if form is valid
    if filter_form.is_valid():
        data = filter_form.cleaned_data

        # Filter by postal code
        if data.get('postal_code'):
            properties = properties.filter(postal_code=data['postal_code'])

        # Filter by price range
        if data.get('min_price'):
            properties = properties.filter(price__gte=data['min_price'])
        if data.get('max_price'):
            properties = properties.filter(price__lte=data['max_price'])

        # Filter by property type
        if data.get('property_type'):
            properties = properties.filter(type=data['property_type'])

        # Search by street name (case-insensitive)
        if data.get('search'):
            # TEMPORARILY use title instead of street_address
            properties = properties.filter(title__icontains=data['search'])

        # Ordering
        if data.get('ordering'):
            properties = properties.order_by(data['ordering'])

    context = {
        'properties': properties,
        'filter_form': filter_form,
    }
    return render(request, 'properties/property_listings.html', context)

def property_details(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    # Get the latest offer for this property from the current user (if logged in)
    user_offer = None
    if request.user.is_authenticated:
        user_offer = PurchaseOffer.objects.filter(
            related_property=property,
            user=request.user
        ).order_by('-date_created').first()

    context = {
        'property': property,
        'user_offer': user_offer,
    }
    return render(request, 'properties/property_details.html', context)


@login_required
def submit_purchase_offer(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    # Check if property is sold
    if property.is_sold:
        messages.error(request, "Cannot submit offer for a sold property")
        return JsonResponse({'success': False, 'message': 'This property is sold and not accepting offers'})

    if request.method == 'POST':
        # Process form submission
        form = PurchaseOfferForm(request.POST)
        if form.is_valid():
            # Check if date is valid (not in the past)
            if form.cleaned_data['expiration_date'] < timezone.now().date():
                return JsonResponse({'success': False, 'message': 'Expiration date cannot be in the past'})

            # Create the purchase offer
            offer = form.save(commit=False)
            # Set the foreign key relationships
            offer.related_property = property
            offer.user = request.user

            # Convert the date to datetime with timezone for date_expired
            offer.date_expired = timezone.datetime.combine(
                form.cleaned_data['expiration_date'],
                timezone.datetime.min.time()
            ).replace(tzinfo=timezone.get_current_timezone())

            offer.save()

            return JsonResponse({'success': True, 'message': 'Your purchase offer has been submitted'})
        else:
            return JsonResponse({'success': False, 'message': form.errors.as_text()})

    # This view only handles POST requests
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
#Login required to favorite a listing
def favorite_listings(request, property_id):
    favorite_property = get_object_or_404(Property, id=property_id)
    request.user.favorite_properties.add(favorite_property)
    request.user.save()
    return redirect('properties:property_details', property_id=property_id)

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Property
from .forms import PropertyFilterForm
from offers.models import PurchaseOffer
from offers.forms import PurchaseOfferForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import UserFavorite


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
            search_query = data['search']
            properties = properties.filter(
                Q(street_address__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(postal_code__icontains=search_query) |
                Q(title__icontains=search_query)
            )

        # Ordering
        if data.get('ordering'):
            properties = properties.order_by(data['ordering'])

    # Get favorite IDs if user is logged in
    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = UserFavorite.objects.filter(user=request.user).values_list('property_id', flat=True)

    context = {
        'properties': properties,
        'filter_form': filter_form,
        'favorite_ids': list(favorite_ids),
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

        # Get user's favorite property Ids
        favorite_ids = UserFavorite.objects.filter(user=request.user).values_list('property_id', flat=True)
    else:
        favorite_ids = []

    # Pre-calculate is_sold status
    is_sold = property.status == 'Sold'

    context = {
        'property': property,
        'user_offer': user_offer,
        'is_sold': is_sold,
        'favorite_ids': list(favorite_ids),

    }
    return render(request, 'properties/property_details.html', context)


#Login required to favorite a listing
@login_required
def favorite_listings(request, property_id):
    favorite_property = get_object_or_404(Property, id=property_id)
    request.user.favorite_properties.add(favorite_property)
    request.user.save()
    return redirect('properties:property_details', property_id=property_id)


@login_required
def submit_purchase_offer(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    # Check if user is a seller - don't allow sellers to make offers
    if hasattr(request.user, 'profile') and request.user.profile.is_seller:
        messages.error(request, "As a seller, you cannot submit purchase offers.")
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Sellers cannot submit purchase offers'})
        return redirect('properties:property_details', property_id=property.id)

    # Check if property is sold
    if property.is_sold:
        messages.error(request, "Cannot submit offer for a sold property")
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'This property is sold and not accepting offers'})
        return redirect('properties:property_details', property_id=property.id)

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

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django import forms  # Add this import here
from .forms import PurchaseFinalizationForm, PurchaseOfferForm
from .models import PurchaseOffer, PurchaseFinalization
from properties.models import Property
from django.utils import timezone
from sellers.models import Seller


@login_required
def purchase_offers_list(request):
    # Get all offers from the current user
    offers = PurchaseOffer.objects.filter(user=request.user).order_by('-date_created')
    # Get the properties for these offers
    properties = [offer.related_property for offer in offers]

    # Get favorite IDs from UserFavorite table
    favorite_ids = []
    if request.user.is_authenticated:
        from accounts.models import UserFavorite
        favorite_ids = UserFavorite.objects.filter(user=request.user).values_list('property_id', flat=True)

    return render(request, 'offers/purchase_offers_list.html', {
        'offers': offers,
        'properties': properties,
        'favorite_ids': favorite_ids,
    })


@login_required
def seller_offers_list(request):
    # Check if user is a seller
    if not hasattr(request.user, 'profile') or not request.user.profile.is_seller:
        messages.error(request, "You don't have seller privileges.")
        return redirect('home')

    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        # This is a critical issue - the user is marked as a seller but doesn't have a Seller record
        # Let's create one with basic details to avoid breaking the flow
        seller = Seller.objects.create(
            user=request.user,
            name=request.user.username,
            email=request.user.email
        )
        messages.warning(request, "Your seller profile has been automatically created.")

    # Get all properties for this seller
    seller_properties = Property.objects.filter(seller=seller)

    # Get offers for these properties
    properties_with_offers = {}

    for prop in seller_properties:
        offers = PurchaseOffer.objects.filter(related_property=prop).order_by('-date_created')
        if offers.exists():
            properties_with_offers[prop.id] = {
                'property': prop,
                'offers': list(offers)
            }

    return render(request, 'offers/seller_offers_list.html', {
        'properties_with_offers': properties_with_offers.values()
    })


@login_required
def respond_to_offer(request, offer_id):
    # Get the offer
    offer = get_object_or_404(PurchaseOffer, id=offer_id)

    # Check if user is a seller
    if not hasattr(request.user, 'profile') or not request.user.profile.is_seller:
        messages.error(request, "You don't have seller privileges.")
        return redirect('home')

    # Get seller for this user
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        messages.error(request, "Your seller profile is not properly set up.")
        return redirect('home')

    # Check if this seller owns the property
    if offer.seller != seller:
        messages.error(request, "You don't have permission to respond to this offer.")
        return redirect('offers:myoffers')

    # Check if the property is sold
    if offer.related_property.status == 'Sold':
        messages.error(request, "This property has been sold and offers can no longer be updated.")
        return redirect('offers:myoffers')

    if request.method == 'POST':
        response = request.POST.get('response')

        if response == 'accept':
            # Accept this offer
            offer.status = 'Accepted'
            offer.save()

            # Reject all other pending offers for this property
            PurchaseOffer.objects.filter(
                related_property=offer.related_property,
                status='Pending'
            ).exclude(id=offer.id).update(status='Rejected')

            messages.success(request, "You've accepted the offer.")

        elif response == 'reject':
            # Reject this offer
            offer.status = 'Rejected'
            offer.save()
            messages.success(request, "You've rejected the offer.")

        elif response == 'contingent':
            # Mark as contingent
            offer.status = 'Contingent'
            offer.save()
            messages.success(request, "You've marked the offer as contingent.")

        return redirect('offers:myoffers')

    return render(request, 'offers/respond_to_offer.html', {'offer': offer})


@login_required
def submit_purchase_offer(request, property_id):
    property = get_object_or_404(Property, id=property_id)

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
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Expiration date cannot be in the past'})
                messages.error(request, "Expiration date cannot be in the past")
                return render(request, 'offers/submit_purchase_offer.html', {'form': form, 'property': property})

            # Create the purchase offer
            offer = form.save(commit=False)

            # Set the required fields
            offer.related_property = property
            offer.user = request.user
            offer.property_name = property.title
            offer.seller = property.seller

            # Set seller_name directly from the seller object
            if property.seller:
                offer.seller_name = property.seller.name
            else:
                offer.seller_name = "Unknown"  # Fallback if no seller is assigned

            # Convert the date to datetime with timezone for date_expired
            offer.date_expired = timezone.datetime.combine(
                form.cleaned_data['expiration_date'],
                timezone.datetime.min.time()
            ).replace(tzinfo=timezone.get_current_timezone())

            offer.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(
                    {'success': True, 'message': 'Your purchase offer has been submitted successfully!'})

            messages.success(request, "Your purchase offer has been submitted successfully!")
            return redirect('properties:property_details', property_id=property.id)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': form.errors.as_text()})

            return render(request, 'offers/submit_purchase_offer.html', {'form': form, 'property': property})

    # GET request - display the form
    form = PurchaseOfferForm()
    return render(request, 'offers/submit_purchase_offer.html', {'form': form, 'property': property})


@login_required
def contact_info_view(request, offer_id):
    """First step of the finalization process - collecting contact information"""
    offer = get_object_or_404(PurchaseOffer, id=offer_id, user=request.user)
    # Use related_property instead of property
    property = offer.related_property

    # Check if offer can be finalized
    if not offer.can_finalize:
        messages.error(request, "This offer cannot be finalized at this time.")
        return redirect('offers:offers')

    # Initialize existing_finalization to None first
    existing_finalization = None

    # Check if an existing finalization exists
    try:
        existing_finalization = PurchaseFinalization.objects.get(purchase_offer=offer)
        initial_data = {
            'street_address': existing_finalization.street_address,
            'city': existing_finalization.city,
            'postal_code': existing_finalization.postal_code,
            'country': existing_finalization.country,
            'national_id': existing_finalization.national_id,
        }
    except PurchaseFinalization.DoesNotExist:
        # Try to get data from session if no finalization exists
        if 'finalization_contact_info' in request.session:
            initial_data = request.session['finalization_contact_info']
        else:
            initial_data = {}

    # Create a form with only the contact fields
    class ContactInfoForm(forms.ModelForm):
        class Meta:
            model = PurchaseFinalization
            fields = ['street_address', 'city', 'postal_code', 'country', 'national_id']

    if request.method == 'POST':
        form = ContactInfoForm(request.POST)

        if form.is_valid():
            # Store form data in session
            request.session['finalization_contact_info'] = {
                'street_address': form.cleaned_data['street_address'],
                'city': form.cleaned_data['city'],
                'postal_code': form.cleaned_data['postal_code'],
                'country': form.cleaned_data['country'],
                'national_id': form.cleaned_data['national_id'],
            }

            # If finalization exists, update it
            if existing_finalization:
                existing_finalization.street_address = form.cleaned_data['street_address']
                existing_finalization.city = form.cleaned_data['city']
                existing_finalization.postal_code = form.cleaned_data['postal_code']
                existing_finalization.country = form.cleaned_data['country']
                existing_finalization.national_id = form.cleaned_data['national_id']
                existing_finalization.save()
            else:
                # Create a new finalization object if one doesn't exist
                finalization = PurchaseFinalization(
                    purchase_offer=offer,
                    street_address=form.cleaned_data['street_address'],
                    city=form.cleaned_data['city'],
                    postal_code=form.cleaned_data['postal_code'],
                    country=form.cleaned_data['country'],
                    national_id=form.cleaned_data['national_id']
                )
                finalization.save()

            # Redirect to payment method page
            return redirect('offers:payment_method', offer_id=offer_id)
    else:
        # Initialize form with saved data
        form = ContactInfoForm(initial=initial_data)

    return render(request, 'offers/contact_info.html', {
        'form': form,
        'offer': offer,
        'property': property,
    })


@login_required
def payment_method_view(request, offer_id):
    """Second step of the finalization process - payment method"""
    offer = get_object_or_404(PurchaseOffer, id=offer_id, user=request.user)

    # Check if offer can be finalized
    if not offer.can_finalize:
        messages.error(request, "This offer cannot be finalized at this time.")
        return redirect('offers:offers')

    # Check if contact info is in session
    if 'finalization_contact_info' not in request.session:
        messages.warning(request, "Please complete the contact information first.")
        return redirect('offers:contact_info', offer_id=offer.id)

    # Get or create finalization object with contact info
    contact_info = request.session['finalization_contact_info']

    try:
        finalization = PurchaseFinalization.objects.get(purchase_offer=offer)
        # Update contact info to make sure it's current
        finalization.street_address = contact_info['street_address']
        finalization.city = contact_info['city']
        finalization.postal_code = contact_info['postal_code']
        finalization.country = contact_info['country']
        finalization.national_id = contact_info['national_id']
        finalization.save()
    except PurchaseFinalization.DoesNotExist:
        # Create new finalization with contact info
        finalization = PurchaseFinalization.objects.create(
            purchase_offer=offer,
            street_address=contact_info['street_address'],
            city=contact_info['city'],
            postal_code=contact_info['postal_code'],
            country=contact_info['country'],
            national_id=contact_info['national_id']
        )

    if request.method == 'POST':
        # Create a dict with contact info to combine with POST data
        # This ensures contact info is preserved during form validation
        form_data = request.POST.copy()

        # Add the contact info to the form data
        form_data.update({
            'street_address': contact_info['street_address'],
            'city': contact_info['city'],
            'postal_code': contact_info['postal_code'],
            'country': contact_info['country'],
            'national_id': contact_info['national_id'],
        })

        form = PurchaseFinalizationForm(form_data, instance=finalization)

        if form.is_valid():
            # Save payment info to finalization object
            finalization = form.save()

            # Redirect to review page
            return redirect('offers:review_purchase', finalization_id=finalization.id)
        else:
            # If there are validation errors, print them for debugging
            print("Form errors:", form.errors)
    else:
        form = PurchaseFinalizationForm(instance=finalization)

    return render(request, 'offers/payment_method.html', {
        'form': form,
        'offer': offer
    })


@login_required
def review_purchase(request, finalization_id):
    """View to review a purchase finalization (read-only)"""
    finalization = get_object_or_404(PurchaseFinalization, id=finalization_id)

    # Make sure the user owns this finalization
    if finalization.purchase_offer.user != request.user:
        messages.error(request, "You don't have permission to view this finalization.")
        return redirect('offers:purchase_offers_list')

    # Get the offer from the finalization
    offer = finalization.purchase_offer

    # Store the contact info back in session for when user navigates back to payment method
    # This ensures the back button will work properly
    request.session['finalization_contact_info'] = {
        'street_address': finalization.street_address,
        'city': finalization.city,
        'postal_code': finalization.postal_code,
        'country': finalization.country,
        'national_id': finalization.national_id,
    }

    return render(request, 'offers/review_purchase.html', {
        'finalization': finalization,
        'offer': offer  # Add the offer to the context
    })


@login_required
def purchase_confirmation(request, finalization_id):
    """Display the purchase confirmation page"""
    finalization = get_object_or_404(PurchaseFinalization, id=finalization_id)

    # Make sure the user owns this finalization
    if finalization.purchase_offer.user != request.user:
        messages.error(request, "You don't have permission to view this finalization.")
        return redirect('offers:purchase_offers_list')

    # Get the offer from the finalization
    offer = finalization.purchase_offer

    # Mark the finalization as completed
    finalization.completed = True
    finalization.save()

    return render(request, 'offers/purchase_confirmation.html', {
        'offer': offer,
        'finalization': finalization
    })

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PurchaseFinalizationForm, PurchaseOfferForm
from .models import PurchaseOffer, PurchaseFinalization
from properties.models import Property
from django.utils import timezone
from sellers.models import Seller

@login_required
def purchase_offers_list(request):
    # Get all offers from the current user
    offers = PurchaseOffer.objects.filter(user=request.user).order_by('-date_created')

    return render(request, 'offers/purchase_offers_list.html', {
        'offers': offers
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
            name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            email=request.user.email
        )
        messages.warning(request, "Your seller profile has been automatically created.")

    # Get all properties for this seller
    from properties.models import Property
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

    # Only allow responding to pending offers
    if offer.status != 'Pending':
        messages.error(request, "This offer has already been processed.")
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
                return JsonResponse({'success': True, 'message': 'Your purchase offer has been submitted successfully!'})
            
            messages.success(request, "Your purchase offer has been submitted successfully!")
            return redirect('properties:property_details', property_id=property.id)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': form.errors.as_text()})
            
            return render(request, 'offers/submit_purchase_offer.html', {'form': form, 'property': property})

    # GET request - display the form
    form = PurchaseOfferForm()
    return render(request, 'offers/submit_purchase_offer.html', {'form': form, 'property': property})

# @login_required
# def cancel_offer(request, offer_id):
#     offer = get_object_or_404(PurchaseOffer, id=offer_id, user=request.user)
#
#     # Only pending offers can be cancelled
#     if offer.status != 'Pending':
#         messages.error(request, "Only pending offers can be cancelled.")
#         return redirect('offers:purchase_offers_list')
#
#     if request.method == 'POST':
#         # Update the offer status to Cancelled
#         offer.status = 'Cancelled'
#         offer.save()
#         messages.success(request, "Your purchase offer has been cancelled successfully.")
#
#     return redirect('offers:purchase_offers_list')


# Create your views here.
@login_required
def finalize_purchase(request, offer_id):
    # Add user ownership check
    purchase_offer = get_object_or_404(PurchaseOffer, id=offer_id, user=request.user)

    # Check if offer can be finalized
    if purchase_offer.status not in ['Accepted', 'Contingent']:
        messages.error(request, "This offer cannot be finalized at this time.")
        return redirect('offers:purchase_offers_list')

    # Check if finalization already exists
    existing_finalization = PurchaseFinalization.objects.filter(purchase_offer=purchase_offer).first()

    if request.method == 'POST':
        # If finalization exists, update it rather than create a new one
        if existing_finalization:
            form = PurchaseFinalizationForm(request.POST, instance=existing_finalization)
        else:
            form = PurchaseFinalizationForm(request.POST)

        if form.is_valid():
            finalization = form.save(commit=False)

            # Only set the purchase_offer if this is a new finalization
            if not existing_finalization:
                finalization.purchase_offer = purchase_offer

            finalization.save()
            return redirect('offers:review_purchase', finalization_id=finalization.id)
    else:
        # Check if finalization already exists
        if existing_finalization:
            form = PurchaseFinalizationForm(instance=existing_finalization)
            messages.info(request, "You're continuing an existing finalization process.")
        else:
            form = PurchaseFinalizationForm()

    return render(request, 'offers/finalize_purchase.html', {
        'form': form,
        'offer': purchase_offer
    })


@login_required
def review_purchase(request, finalization_id):
    """View to review a purchase finalization (read-only)"""
    finalization = get_object_or_404(PurchaseFinalization, id=finalization_id)

    # Make sure the user owns this finalization
    if finalization.purchase_offer.user != request.user:
        messages.error(request, "You don't have permission to view this finalization.")
        return redirect('offers:purchase_offers_list')

    return render(request, 'offers/review_purchase.html', {
        'finalization': finalization
    })

@login_required
def confirm_purchase(request, finalization_id):
    """Handle the final purchase confirmation"""
    finalization = get_object_or_404(PurchaseFinalization, id=finalization_id)

    # Make sure the user owns this finalization
    if finalization.purchase_offer.user != request.user:
        messages.error(request, "You don't have permission to confirm this purchase.")
        return redirect('offers:purchase_offers_list')

    offer = finalization.purchase_offer

    if request.method == 'POST':
        # Check if terms agreement checkbox was checked
        if 'terms_agreement' in request.POST:
            # Mark the finalization as completed
            finalization.completed = True
            finalization.save()
            # The model's save method will update the offer and property status
            messages.success(request, "Purchase has been successfully finalized!")
            return redirect('offers:purchase_confirmation', offer_id=offer.id)
        else:
            messages.error(request, 'You must agree to the terms to proceed.')
            return redirect('offers:review_purchase', finalization_id=finalization_id)

    # If not a POST request, redirect back to review page
    return redirect('offers:review_purchase', finalization_id=finalization_id)


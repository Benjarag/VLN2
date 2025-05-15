# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse

from accounts.forms import UserUpdateForm, ProfileUpdateForm, CustomUserCreationForm, SellerForm
from django.contrib import messages
from django.contrib.auth import logout, login

from accounts.models import Profile, UserFavorite
from properties.models import Property
from django.views.decorators.http import require_POST

from sellers.models import Seller



@login_required
def profile(request):
    if request.user.profile.is_seller:
        print("User is a seller")
    else:
        print("user is a buyer")

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_update(request):
    seller_form = None
    is_user_seller = request.user.profile.is_seller

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        is_still_seller = 'is_seller' in request.POST

        if is_user_seller or is_still_seller:
            seller, created = Seller.objects.get_or_create(user=request.user)
            seller_form = SellerForm(request.POST, request.FILES, instance=seller)

            if user_form.is_valid() and profile_form.is_valid() and seller_form.is_valid():
                user = user_form.save()

                new_profile = profile_form.save(commit=False)
                new_profile.is_seller = True
                new_profile.save()

                seller.email = user.email
                seller.name = user.username

                # If profile has an image, use it for seller cover image
                if new_profile.image:
                    seller.cover_image = new_profile.image

                seller_form.save()

                messages.success(request, 'Your seller profile has been updated successfully!')
                return redirect('accounts:profile')
            else:
                # Add specific error messages for invalid forms
                for form_name, form in [("User form", user_form),
                                        ("Profile form", profile_form),
                                        ("Seller form", seller_form)]:
                    if not form.is_valid():
                        for field, errors in form.errors.items():
                            for error in errors:
                                messages.error(request, f"{form_name} - {field}: {error}")

                messages.error(request,
                               'There was an error updating your profile. Please check the form and try again.')
        else:
            # User is not a seller, just handle the user and profile forms
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                profile = profile_form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('accounts:profile')
            else:
                messages.error(request,
                               'There was an error updating your profile. Please check the form and try again.')
    else:
        # GET request - initialize forms
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

        # Initialize seller form if user is a seller
        if is_user_seller:
            seller, created = Seller.objects.get_or_create(user=request.user)
            seller_form = SellerForm(instance=seller)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    # Add seller_form to context if it exists
    if seller_form is not None:
        context['seller_form'] = seller_form

    return render(request, 'accounts/profile_update.html', context)


@require_POST
def toggle_favorite(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'guest-user'})

    property_id = request.POST.get('property_id')
    property_obj = get_object_or_404(Property, id=property_id)
    user = request.user

    favorite_exists = UserFavorite.objects.filter(user=user, property=property_obj).exists()

    if favorite_exists:
        UserFavorite.objects.filter(user=user, property=property_obj).delete()
        return JsonResponse({'status': 'removed'})
    else:
        UserFavorite.objects.create(user=user, property=property_obj)
        return JsonResponse({'status': 'added'})

@login_required
def favorites_view(request):
    favorite_property_id = UserFavorite.objects.filter(user=request.user).values_list('property_id', flat=True)
    favorites = Property.objects.filter(id__in=favorite_property_id)

    return render(request, 'accounts/favorite.html', {'favorites': favorites})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home:homepage')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save()

            if form.cleaned_data.get('usertype'):
                Seller.objects.create(
                    user=user,
                    name=user.username,
                    type="Individual",
                    email=user.email,
                    phone="",
                    street_address="",
                    city="",
                    postal_code="",
                    logo=None,
                    cover_image=None,
                    bio="",
                )
            # Log the user in
            login(request, user)
            # Redirect to home page
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

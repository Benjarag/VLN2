# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse

from accounts.forms import UserUpdateForm, ProfileUpdateForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import logout, login

from accounts.models import Profile, UserFavorite
from properties.models import Property
from django.views.decorators.http import require_POST


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
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
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'There was an error updating your profile. Please check the form and try again.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/profile_update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

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
            # Create profile if it doesn't exist (we don't need to store the profile object)
            # Just using get_or_create to ensure it exists
            Profile.objects.get_or_create(user=user)
            # Log the user in
            login(request, user)
            # Redirect to home page
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

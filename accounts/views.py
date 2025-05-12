# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from accounts.forms import UserUpdateForm, ProfileUpdateForm, CustomUserCreationForm
from django.contrib import  messages
from django.contrib.auth import logout, login

from accounts.models import Profile
from properties.models import Property


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


def toggle_favorite(request):
    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        property_obj = get_object_or_404(Property, id=property_id)

        user = request.user

        if property_obj in user.favorite_properties.all():
            # ef hann ýtir á favorite takkann þegar búið er að favorite-a listing-ið
            user.favorite_properties.remove(property_obj)
            return JsonResponse({'status': 'removed'})
        else:
            user.favorite_properties.add(property_obj)
            return JsonResponse({'status': 'added'})
    return JsonResponse({'error': 'Bad request'}, status=400)

def favorites_view(request):
    properties = request.user.favorite_properties.all()
    return render(request, 'accounts/favorite.html', {'properties': properties})

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

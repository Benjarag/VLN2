from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from sellers.models import Seller
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'signup_email', 'placeholder': 'Email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'signup_username', 'placeholder': 'Username'})
    )

    usertype = forms.BooleanField(
        required=False,
        label='I am a seller',
        help_text='Check this box if you are a seller'
    )

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'signup_password1', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'id': 'signup_password2', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.is_seller = self.cleaned_data["usertype"]
            profile.save()
        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'login_username',
            'placeholder': 'Username'
        }))
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'login_password',
            'placeholder': 'Password'
        }))


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(help_text='')  # Empty help text

    class Meta:
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'phone', 'is_seller']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_seller': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class SellerUpdateForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['type', 'phone', 'logo', 'cover_image', 'bio', 'street_address', 'city', 'postal_code']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'})
        }


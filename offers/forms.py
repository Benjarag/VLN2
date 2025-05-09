# forms.py
from django import forms
from django.utils import timezone
from .models import PurchaseFinalization, PurchaseOffer


class PurchaseOfferForm(forms.ModelForm):
    # Override the offer_price field to add validation and styling
    offer_price = forms.IntegerField(
        label="Offer Price (ISK)",
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your offer amount in ISK'
        })
    )

    # Add a date picker for expiration date
    expiration_date = forms.DateField(
        label="Offer Expiration Date",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': timezone.now().date().isoformat()  # Set minimum date to today
        })
    )

    class Meta:
        model = PurchaseOffer
        fields = ['offer_price', 'expiration_date']


class PurchaseFinalizationForm(forms.ModelForm):
    class Meta:
        model = PurchaseFinalization
        fields = [
            'street_address', 'city', 'postal_code', 'country', 'national_id',
            'payment_option',
            'cardholder_name', 'credit_card_number', 'credit_card_expiry', 'credit_card_cvc',
            'bank_account',
            'mortgage_provider'
        ]
        widgets = {
            'payment_option': forms.RadioSelect(),
            'mortgage_provider': forms.Select(),
        }

    def clean(self):
        cleaned_data = super().clean()
        payment_option = cleaned_data.get('payment_option')
        
        if payment_option == 'Credit Card':
            # Validate credit card fields
            if not cleaned_data.get('cardholder_name'):
                self.add_error('cardholder_name', 'Required for credit card payment')
            if not cleaned_data.get('credit_card_number'):
                self.add_error('credit_card_number', 'Required for credit card payment')
            # Add validation for other credit card fields
            
        elif payment_option == 'Bank Transfer':
            # Validate bank transfer fields
            if not cleaned_data.get('bank_account'):
                self.add_error('bank_account', 'Required for bank transfer')
                
        elif payment_option == 'Mortgage':
            # Validate mortgage fields
            if not cleaned_data.get('mortgage_provider'):
                self.add_error('mortgage_provider', 'Required for mortgage payment')
        
        return cleaned_data


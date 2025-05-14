# forms.py
from django import forms
from django.utils import timezone
from .models import PurchaseFinalization, PurchaseOffer
from .models import PurchaseOffer


class PurchaseOfferForm(forms.ModelForm):
    # Add these fields to the form
    offer_price = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter your offer amount in ISK'})
    )
    expiration_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = PurchaseOffer
        fields = ['offer_price']

    def __init__(self, *args, **kwargs):
        super(PurchaseOfferForm, self).__init__(*args, **kwargs)
        # Set minimum date for expiration date
        self.fields['expiration_date'].initial = timezone.now().date() + timezone.timedelta(days=7)


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

    

class CreditCardForm(forms.Form):
    cardholder_name = forms.CharField(label="Cardholder Name", max_length=100)
    credit_card_number = forms.CharField(label="Card Number", max_length=25)  # Increased to handle formatting
    credit_card_expiry = forms.CharField(label="Expiry Date (MM/YY)", max_length=5)
    credit_card_cvc = forms.CharField(label="CVC", max_length=4)
    
    def clean_credit_card_number(self):
        """Remove formatting characters before validation"""
        return self.cleaned_data['credit_card_number'].replace(' ', '').replace('-', '')
    
    def clean_credit_card_expiry(self):
        """Validate expiry date format"""
        expiry = self.cleaned_data['credit_card_expiry']
        if '/' not in expiry:
            raise forms.ValidationError("Please enter the expiry date in MM/YY format")
        return expiry
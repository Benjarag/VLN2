from django import forms
from django.utils import timezone
from .models import PurchaseFinalization, PurchaseOffer
from .models import PurchaseOffer

from django import forms
import re
from datetime import datetime


class PurchaseOfferForm(forms.ModelForm):
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
    def __init__(self, *args, **kwargs):
        super(PurchaseFinalizationForm, self).__init__(*args, **kwargs)

        # Make the payment_option field required
        self.fields['payment_option'].required = True

        # Payment fields as required=False initially (we'll validate them conditionally)
        self.fields['cardholder_name'].required = False
        self.fields['credit_card_number'].required = False
        self.fields['credit_card_expiry'].required = False
        self.fields['credit_card_cvc'].required = False
        self.fields['bank_account'].required = False
        self.fields['mortgage_provider'].required = False

        # Contact fields not required at this stage since they should be filled already
        self.fields['street_address'].required = False
        self.fields['city'].required = False
        self.fields['postal_code'].required = False
        self.fields['country'].required = False
        self.fields['national_id'].required = False

        # If the form is bound and payment_option is selected, set requirements
        if self.is_bound and 'payment_option' in self.data:
            if self.data['payment_option'] == 'Credit Card':
                self.fields['cardholder_name'].required = True
                self.fields['credit_card_number'].required = True
                self.fields['credit_card_expiry'].required = True
                self.fields['credit_card_cvc'].required = True
            elif self.data['payment_option'] == 'Bank Transfer':
                self.fields['bank_account'].required = True
            elif self.data['payment_option'] == 'Mortgage':
                self.fields['mortgage_provider'].required = True

    class Meta:
        model = PurchaseFinalization
        fields = [
            'payment_option',
            'cardholder_name', 'credit_card_number', 'credit_card_expiry', 'credit_card_cvc',
            'bank_account',
            'mortgage_provider',
            # Including contact fields but they won't be shown in the template
            'street_address', 'city', 'postal_code', 'country', 'national_id'
        ]
        widgets = {
            'payment_option': forms.RadioSelect(),
            'mortgage_provider': forms.Select(),
        }

    def clean_credit_card_number(self):
        """Remove formatting characters before saving to database"""
        raw_number = self.cleaned_data.get('credit_card_number', '')
        if not raw_number:
            return raw_number

        # Removing spaces and dashes
        cleaned_number = raw_number.replace(' ', '').replace('-', '')

        # Validating it's a 16-digit number
        if self.cleaned_data.get('payment_option') == 'Credit Card' and not re.match(r'^\d{16}$', cleaned_number):
            raise forms.ValidationError("Credit card number must be 16 digits")

        return cleaned_number

    def clean_credit_card_cvc(self):
        """Validate CVC is a 3-digit number"""
        cvc = self.cleaned_data.get('credit_card_cvc', '')
        if not cvc:
            return cvc

        # Removing any whitespace and non-digits
        cvc = re.sub(r'\D', '', cvc.strip())

        # Validating it's a 3-digit number
        if self.cleaned_data.get('payment_option') == 'Credit Card' and len(cvc) != 3:
            raise forms.ValidationError("CVC must be exactly 3 digits")

        return cvc

    def clean_credit_card_expiry(self):
        """Validate expiry date format and that it's not in the past"""
        expiry = self.cleaned_data.get('credit_card_expiry', '')
        if not expiry or self.cleaned_data.get('payment_option') != 'Credit Card':
            return expiry

        # Check format MM/YY
        if not re.match(r'^\d{2}/\d{2}$', expiry):
            raise forms.ValidationError("Please enter the expiry date in MM/YY format")

        # Parse month and year
        try:
            month, year = expiry.split('/')
            month = int(month)
            year = int('20' + year)  # Convert YY to 20YY

            # Validate month is between 1-12
            if month < 1 or month > 12:
                raise forms.ValidationError("Month must be between 1 and 12")

            # Get current date for comparison
            now = datetime.now()
            current_year = now.year
            current_month = now.month

            # Check if card is expired
            if (year < current_year) or (year == current_year and month < current_month):
                raise forms.ValidationError("The credit card has expired")

        except ValueError:
            raise forms.ValidationError("Invalid expiry date format")

        return expiry

    def clean(self):
        cleaned_data = super().clean()
        payment_option = cleaned_data.get('payment_option')

        if not payment_option:
            self.add_error('payment_option', 'Please select a payment option')
            return cleaned_data

        # Only validate payment-specific fields, not contact info
        if payment_option == 'Credit Card':
            fields = ['cardholder_name', 'credit_card_number', 'credit_card_expiry', 'credit_card_cvc']
            for field in fields:
                if not cleaned_data.get(field):
                    self.add_error(field, f'This field is required for credit card payments')

        elif payment_option == 'Bank Transfer':
            if not cleaned_data.get('bank_account'):
                self.add_error('bank_account', 'Bank account information is required')

        elif payment_option == 'Mortgage':
            if not cleaned_data.get('mortgage_provider'):
                self.add_error('mortgage_provider', 'Please select a mortgage provider')

        return cleaned_data


class CreditCardForm(forms.Form):
    cardholder_name = forms.CharField(
        label="Cardholder Name", 
        max_length=100,
        required=True,
        error_messages={'required': 'Cardholder name is required'}
    )
    credit_card_number = forms.CharField(
        label="Card Number", 
        max_length=25,  # Increased to handle formatting
        required=True,
        error_messages={'required': 'Credit card number is required'}
    )
    credit_card_expiry = forms.CharField(
        label="Expiry Date (MM/YY)", 
        max_length=5,
        required=True,
        error_messages={'required': 'Expiry date is required'}
    )
    credit_card_cvc = forms.CharField(
        label="CVC", 
        max_length=4,
        required=True,
        error_messages={'required': 'CVC is required'}
    )

    def clean_credit_card_number(self):
        """Validate and clean credit card number"""
        raw_number = self.cleaned_data.get('credit_card_number', '')
        if not raw_number:
            raise forms.ValidationError("Credit card number is required")
            
        # Remove spaces and dashes
        cleaned_number = raw_number.replace(' ', '').replace('-', '')
        
        # Validate it's a 16-digit number
        if not re.match(r'^\d{16}$', cleaned_number):
            raise forms.ValidationError("Credit card number must be 16 digits")
            
        return cleaned_number

    def clean_credit_card_expiry(self):
        """Validate expiry date format and that it's not in the past"""
        expiry = self.cleaned_data.get('credit_card_expiry', '')
        if not expiry:
            raise forms.ValidationError("Expiry date is required")
            
        # Check format MM/YY
        if not re.match(r'^\d{2}/\d{2}$', expiry):
            raise forms.ValidationError("Please enter the expiry date in MM/YY format")
            
        # Parse month and year
        try:
            month, year = expiry.split('/')
            month = int(month)
            year = int('20' + year)  # Convert YY to 20YY
            
            # Validate month is between 1-12
            if month < 1 or month > 12:
                raise forms.ValidationError("Month must be between 1 and 12")
                
            # Get current date for comparison
            now = datetime.now()
            current_year = now.year
            current_month = now.month
            
            # Check if card is expired
            if (year < current_year) or (year == current_year and month < current_month):
                raise forms.ValidationError("The credit card has expired")
                
        except ValueError:
            raise forms.ValidationError("Invalid expiry date format")
            
        return expiry

    def clean_credit_card_cvc(self):
        """Validate CVC is a 3-digit number"""
        cvc = self.cleaned_data.get('credit_card_cvc', '')
        if not cvc:
            if self.cleaned_data.get('payment_option') == 'Credit Card':
                raise forms.ValidationError("CVC is required")
            return cvc
        
        # Remove any whitespace and non-digits
        cvc = re.sub(r'\D', '', cvc.strip())
        
        # Validate it's a 3-digit number
        if len(cvc) != 3:
            raise forms.ValidationError("CVC must be exactly 3 digits")
        
        return cvc
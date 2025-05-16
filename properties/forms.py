# properties/forms.py
from django import forms
from .models import Property

class PropertyFilterForm(forms.Form):
    # For the search field, similarly add style
    search = forms.CharField(
        required=False, 
        label='Search by street address',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by street address...',
            'style': 'font-size: 0.60rem;'  # Adjust size as needed
        })
    )
    
    # Postal code field
    postal_code = forms.CharField(required=False, label='Postal Code')
    
    # Price range fields
    min_price = forms.IntegerField(required=False, label='Min Price',
                                  widget=forms.NumberInput(attrs={'placeholder': 'Min'}))
    max_price = forms.IntegerField(required=False, label='Max Price',
                                  widget=forms.NumberInput(attrs={'placeholder': 'Max'}))
    
    # For the property_type field, add a style attribute to make the font smaller
    property_type = forms.ChoiceField(
        choices=[('', '-- Select Property Type --')] + list(Property.PROPERTY_TYPES),
        required=False,
        label='Property Type',
        widget=forms.Select(attrs={'style': 'font-size: 0.60rem;'})  # Adding style for smaller font
    )
    
    
    # Ordering options
    ORDERING_CHOICES = [
        ('', '-- Sort By --'),
        ('price', 'Price (Low to High)'),
        ('-price', 'Price (High to Low)'),
        ('date_listed', 'Date Listed (Oldest First)'),
        ('-date_listed', 'Date Listed (Newest First)'),
        ('size', 'Size (Small to Large)'),
        ('-size', 'Size (Large to Small)'),
    ]
    
    ordering = forms.ChoiceField(
        choices=ORDERING_CHOICES,
        required=False,
        label='Sort By'
    )
    
    def __init__(self, *args, **kwargs):
        super(PropertyFilterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
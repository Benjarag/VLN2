from datetime import timezone

from django.contrib.auth.models import User
from django.db import models
from properties.models import Property


class PurchaseOffer(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Contingent', 'Contingent'),
        # ('Expired', 'Expired'),
        # ('Finalized', 'Finalized'),
        # ('Cancelled', 'Cancelled'),
    ]

    # Add this field
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase_offers')

    # Foreign keys to related models
    related_property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='purchase_offers')
    seller = models.ForeignKey('sellers.Seller', on_delete=models.SET_NULL, null=True, related_name='received_offers')

    # Original text fields
    property_name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_expired = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    seller_name = models.CharField(max_length=255)
    offer_price = models.IntegerField()

    def __str__(self):
        return f'{self.property_name} - {self.status}'

    def is_expired(self):
        """"Return True if the offer is expired"""
        return self.date_expired < timezone.now()

    def get_formatted_price(self):
        """Return the price with the proper formatting with dots as thousands separators"""
        price_str = str(self.offer_price)
        formatted_price = ""
        for i, digit in enumerate(reversed(price_str)):
            if i > 0 and i % 3 == 0:
                formatted_price = "." + formatted_price
            formatted_price = digit + formatted_price

        return f"{formatted_price} kr"

    @property
    def can_finalize(self):
        """Check if offer can be finalized"""
        return self.status in ['Accepted', 'Contingent']

class PurchaseFinalization(models.Model):
    PAYMENT_OPTIONS = [
        ('Credit Card', 'Credit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Mortgage', 'Mortgage'),
    ]

    COUNTRIES = [
        ('Iceland', 'Iceland'),
        ('Norway', 'Norway'),
        ('Sweden', 'Sweden'),
        ('Denmark', 'Denmark'),
        ('Finland', 'Finland'),
        ('Estonia', 'Estonia'),
        ('Lithuania', 'Lithuania'),
        ('Latvia', 'Latvia'),
        ('Poland', 'Poland'),
    ]

    MORTAGE_PROVIDERS = [
        ('Arion Banki', 'Arion Banki'),
        ('Landsbankinn', 'Landsbankinn'),
        ('Islandsbanki', 'Islandsbanki'),
        ('Bank of America', 'Bank of America'),
        ('Bank of Ireland', 'Bank of Ireland'),
        ('Citi', 'Citi'),
        ('HSBC', 'HSBC'),
        ('J.P. Morgan', 'J.P. Morgan'),
        ('Rabobank', 'Rabobank'),
        ('Santander', 'Santander'),
        ('Skandinavian Bank', 'Skandinavian Bank'),
        ('Swedbank', 'Swedbank'),
        ('U.S. Bank', 'U.S. Bank'),
        ('Vestbank', 'Vestbank'),
    ]

    purchase_offer = models.OneToOneField(PurchaseOffer, on_delete=models.CASCADE)

    # Contact information
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, choices=COUNTRIES, default="Iceland")
    national_id = models.CharField(max_length=20, help_text="National ID (kennitala)")

    # Payment information
    payment_option = models.CharField(max_length=50, choices=PAYMENT_OPTIONS)

    # Credit card fields (only used if payment_method is 'Credit Card')
    cardholder_name = models.CharField(max_length=255, blank=True, default="")
    credit_card_number = models.CharField(max_length=25, blank=True, default="")
    credit_card_expiry = models.CharField(max_length=7, blank=True, default="")
    credit_card_cvc = models.CharField(max_length=4, blank=True, default="")

    # Bank Transfer fields (only used if payment_method is 'Bank Transfer')
    bank_account = models.CharField(max_length=50, blank=True, default="",
                                    help_text="IBAN, Swift or Icelandic format")

    # Mortgage fields (only used if payment_method is 'Mortgage')
    mortgage_provider = models.CharField(max_length=100, choices=MORTAGE_PROVIDERS,
                                         blank=True, default="")

    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Finalization for {self.purchase_offer}"

    def save(self, *args, **kwargs):
        """When completed, update the purchase offer status"""
        if self.completed and self.purchase_offer.status != 'Finalized':
            self.purchase_offer.status = 'Finalized'
            self.purchase_offer.save()

            # Also update property status to Sold
            self.purchase_offer.related_property.status = 'Sold'
            self.purchase_offer.related_property.save()

        super().save(*args, **kwargs)
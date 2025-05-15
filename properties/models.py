from django.db import models
from django.urls import reverse
from sellers.models import Seller


class Property(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Sold', 'Sold'),
    ]

    PROPERTY_TYPES = [
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('Townhouse', 'Townhouse'),
        ('Sumarhús', 'Sumarhús'),
        ('Fjölbýlishús', 'Fjölbýlishús'),
        ('Einbýlishús', 'Einbýlishús'),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    size = models.IntegerField(help_text="Size in square meters")
    price = models.IntegerField(help_text="Price in ISK")
    rooms = models.IntegerField()
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Available")
    type = models.CharField(max_length=100, choices=PROPERTY_TYPES)
    date_listed = models.DateField(null=True, blank=True)
    description = models.TextField()

    # Foreign key to Seller instead of embedded data
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='properties', null=True, blank=True)



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Return the absolute URL for the property using ID"""
        return reverse('properties:property_details', kwargs={'property_id': self.id})

    def get_formatted_price(self):
        """Return the price with kr suffix and proper formatting with dots as thousands separators"""
        # Convert price to string
        price_str = str(self.price)

        # Format with dots as thousands separators (starting from right)
        formatted_price = ""
        for i, digit in enumerate(reversed(price_str)):
            if i > 0 and i % 3 == 0:
                formatted_price = "." + formatted_price
            formatted_price = digit + formatted_price

        return formatted_price

    def get_formatted_date(self):
        """Return only the date part (year, month, day) without time"""
        return self.date_listed.strftime('%Y-%m-%d')

    @property
    def has_accepted_offer(self):
        """Check if property has an accepted offer"""
        return self.purchase_offers.filter(status='Accepted').exists()

    @property
    def is_sold(self):
        """Check if property is sold based on status or finalized offer"""
        return self.status == 'Sold' or self.purchase_offers.filter(status='Finalized').exists()


class PropertyImage(models.Model):
    related_property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='properties/images')
    order = models.PositiveIntegerField(default=0)  # to keep track of image order

    class Meta:
        ordering = ['order']  # This will order images based on their "order" field.


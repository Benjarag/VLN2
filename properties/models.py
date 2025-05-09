from django.db import models

class Property(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    size = models.IntegerField(help_text="Size in square meters")
    price = models.IntegerField(help_text="Price in ISK")
    rooms = models.IntegerField()
    bedrooms = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default="Available")
    type = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to='properties/images', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    bathrooms = models.IntegerField()
    description = models.TextField()

    # Add seller information
    seller_name = models.CharField(max_length=255, null=True, blank=True)
    seller_phone = models.CharField(max_length=20, null=True, blank=True)
    seller_profile_image = models.ImageField(upload_to='properties/images', null=True, blank=True)
    
    # Add to your Property model
    zip = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.title
    
    @property
    def seller(self):
        """Return a dictionary with seller information for template access"""
        return {
            'name': self.seller_name,
            'phone': self.seller_phone,
            'profile_image': self.seller_profile_image
        }

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
        return self.date.strftime('%Y-%m-%d')

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='properties/images')
    order = models.PositiveIntegerField(default=0)  # to keep track of image order

    class Meta:
        ordering = ['order']  # This will order images based on their "order" field.
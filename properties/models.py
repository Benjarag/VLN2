from django.db import models

class Property(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    size = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.IntegerField()
    status = models.BooleanField(default=True)
    type = models.CharField(max_length=100)
    bathrooms = models.IntegerField()
    description = models.TextField()
    address = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    # Add seller information
    seller_name = models.CharField(max_length=255, null=True, blank=True)
    seller_phone = models.CharField(max_length=20, null=True, blank=True)
    seller_profile_image = models.ImageField(upload_to='seller_images/', null=True, blank=True)

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    order = models.PositiveIntegerField(default=0)  # to keep track of image order

    class Meta:
        ordering = ['order']  # This will order images based on their "order" field.

from django.db import models

class Property(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='property_images/')
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    description = models.TextField()
    is_published = models.BooleanField(default=True)
    badges = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



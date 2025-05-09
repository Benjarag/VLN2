# from django.db import models
#
#
# class Seller(models.Model):
#     SELLER_TYPES = [
#         ('Individual', 'Individual'),
#         ('Real Estate Agency', 'Real Estate Agency'),
#     ]
#
#     name = models.CharField(max_length=255)
#     type = models.CharField(max_length=100, choices=SELLER_TYPES, default="Individual")
#     phone = models.CharField(max_length=20, blank=True)
#     email = models.EmailField(blank=True, null=True)
#
#     # Address fields (only for agencies)
#     street_address = models.CharField(max_length=255, blank=True, null=True)
#     city = models.CharField(max_length=100, blank=True, null=True)
#     postal_code = models.CharField(max_length=10, blank=True, null=True)
#
#     logo = models.ImageField(upload_to='sellers/images/logos', blank=True, null=True)
#     # Cover image (same as profile image)
#     cover_image = models.ImageField(upload_to='sellers/images/profile_images', blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#
#
#     def __str__(self):
#         return self.name
#
#     @property
#     def show_address(self):
#         """Only show address if seller is a Real Estate Agency"""
#         return self.type == 'Real Estate Agency'
#
#     @property
#     def active_properties(self):
#         """Return properties that are not sold"""
#         # we need this to list the properties on sale by seller when you view the seller profile
#         return self.properties.exclude(status='Sold')

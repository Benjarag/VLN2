from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # here we are storing the user in the profile
    image = models.ImageField(upload_to='profiles/', blank=True, null=True) # here we are storing the image in the profiles folder
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile Page'
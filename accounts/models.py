from django.contrib.auth.models import User
from django.db import models
from django.template.context_processors import request

from properties.models import Property


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # here we are storing the user in the profile
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)  # here we are storing the image in the profiles folder
    phone = models.CharField(max_length=20, blank=True)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile Page'


User.add_to_class('favorite_properties', models.ManyToManyField(Property, related_name='favorited_by_user', blank=True))

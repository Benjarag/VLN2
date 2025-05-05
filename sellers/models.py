from django.db import models

# Create your models here.
# sellers/models.py
from django.db import models

class Seller(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

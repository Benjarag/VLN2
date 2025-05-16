from django.db import models
from django.utils import timezone

# Create your models here.
class Email(models.Model):
    buyer = models.EmailField()
    seller = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date_sent = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default="sent")


    def __str__(self):
        return f"the seller: {self.seller} is sending {self.buyer} an email about {self.subject}"

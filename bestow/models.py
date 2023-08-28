from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Filter(models.Model):
    age = models.CharField(max_length=300)
    gender = models.CharField(max_length=300)
    relationship = models.CharField(max_length=300)
    price_range = models.CharField(max_length=300)
    occasion = models.CharField(max_length=300)
    gift_type = models.CharField(max_length=300)
    interest = models.CharField(max_length=300)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="filters", blank=True, null=True)

    def __str__(self):
        return str(self.id)
from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    date_joined = models.DateTimeField()
    is_vendor = models.BooleanField()
    role = models.BooleanField()

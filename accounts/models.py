from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username=None
    email=models.CharField(unique=True)

    accountType = models.CharField(max_length=50, choices=[("Freelancer", "Freelancer"), ("Company", "Company")])
    country = models.CharField(max_length=100, blank=True, null=True)
    countryCode = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phoneNumber = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.email
    

    

from django.db import models
from django.conf import settings
from wallet.models import *

class Account(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="accounts")
    account_holder = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    routing_number = models.CharField(max_length=50, blank=True, null=True)
    account_type = models.CharField(max_length=50)  
    address = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=10, default="USD")
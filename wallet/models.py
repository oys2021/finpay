from django.db import models
from django.conf import settings

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet")

    def __str__(self):
        return f"{self.user.email}'s Wallet"


class WalletBalance(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="balances")
    currency = models.CharField(max_length=10)  
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        unique_together = ("wallet", "currency")

    def __str__(self):
        return f"{self.wallet.user.email} - {self.currency}: {self.balance}"


class Account(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="accounts")
    account_holder = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    routing_number = models.CharField(max_length=50, blank=True, null=True)
    account_type = models.CharField(max_length=50)  
    address = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=10, default="USD")
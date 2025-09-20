from django.db import models
from django.db import models
from django.conf import settings
import uuid
from wallet.models import Wallet

# class Wallet(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet")
#     currency = models.CharField(max_length=10, default="USD")
#     balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)

#     def __str__(self):
#         return f"{self.user.email}'s Wallet"


class VirtualCard(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("blocked", "Blocked"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="cards")
    reference = models.CharField(max_length=255, unique=True)
    card_reference = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=20, default="virtual")  # virtual/debit/credit
    currency = models.CharField(max_length=10, default="USD")
    holder_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=50)  # Visa, Mastercard
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=2)
    first_six = models.CharField(max_length=6)
    last_four = models.CharField(max_length=4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.holder_name} - {self.brand} ({self.last_four})"

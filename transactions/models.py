
import uuid
from django.db import models
from django.conf import settings

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("INCOME", "Income"),
        ("EXPENSE", "Expense"),
        ("TRANSFER", "Transfer"),
        ("CONVERSION", "Conversion"),
    )
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("successful", "Successful"),
        ("failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    transactionDate = models.DateTimeField(auto_now_add=True)
    amountReceived = models.DecimalField(max_digits=20, decimal_places=2)
    receivingCurrency = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    account_type = models.CharField(max_length=50, null=True, blank=True)  
    account_id = models.CharField(max_length=100, null=True, blank=True)  
    agent_phone_number = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.receivingCurrency} on {self.transactionDate}"
    


import uuid
from django.db import models
from django.conf import settings

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    transactionDate = models.DateTimeField(auto_now_add=True)
    amountReceived = models.DecimalField(max_digits=20, decimal_places=2)
    receivingCurrency = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.receivingCurrency} on {self.transactionDate}"

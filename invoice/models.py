from django.db import models
from django.conf import settings
import uuid

class Invoice(models.Model):
    STATUS_CHOICES = [
        ("due", "Due"),
        ("overdue", "Overdue"),
        ("paid", "Paid"),
        ("pending", "Pending"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invoices")
    currency = models.CharField(max_length=10, default="USD")
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="due")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.user.email}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    description = models.TextField()
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=18, decimal_places=2)  

    def __str__(self):
        return f"{self.description} ({self.quantity} x {self.amount})"
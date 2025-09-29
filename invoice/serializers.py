from rest_framework import serializers
from invoice.models import Invoice, InvoiceItem

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ["description", "quantity", "amount"]

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ["id", "customer","items", "currency", "issue_date", "due_date", "status"]

    def get_customer(self, obj):
        user = obj.user
        return {
            "name": user.get_full_name() or user.name,
            "email": user.email,
            "country": getattr(user, "country", ""),
            "state": getattr(user, "state", ""),
            "address": getattr(user, "address", "")
        }

from rest_framework import serializers
from accounts.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "currency",
            "account_holder",
            "bank_name",
            "account_number",
            "routing_number",
            "account_type",
            "address",
        ]
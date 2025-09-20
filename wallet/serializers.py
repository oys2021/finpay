from rest_framework import serializers

class UserBalanceSerializer(serializers.Serializer):
    total = serializers.CharField()
    usd = serializers.CharField(required=False)
    gbp = serializers.CharField(required=False)
    eur = serializers.CharField(required=False)
    ngn = serializers.CharField(required=False)
    currency = serializers.CharField()


from .models import Account

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
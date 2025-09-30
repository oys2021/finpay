from rest_framework import serializers
from wallet.models import *

class UserBalanceSerializer(serializers.Serializer):
    total = serializers.CharField()
    usd = serializers.CharField(required=False)
    gbp = serializers.CharField(required=False)
    eur = serializers.CharField(required=False)
    ngn = serializers.CharField(required=False)
    currency = serializers.CharField()


class WalletBalanceSerializer(serializers.ModelSerializer):
    accountHolder = serializers.CharField(source="wallet.user.get_full_name", read_only=True)
    bankName = serializers.SerializerMethodField()
    accountNumber = serializers.SerializerMethodField()

    class Meta:
        model = WalletBalance
        fields = ["id", "accountHolder", "bankName", "accountNumber", "currency", "balance"]

    def get_bankName(self, obj):
        return "Demo Bank"

    def get_accountNumber(self, obj):
        return f"ACC{obj.id:06d}"



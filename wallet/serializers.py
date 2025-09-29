from rest_framework import serializers

class UserBalanceSerializer(serializers.Serializer):
    total = serializers.CharField()
    usd = serializers.CharField(required=False)
    gbp = serializers.CharField(required=False)
    eur = serializers.CharField(required=False)
    ngn = serializers.CharField(required=False)
    currency = serializers.CharField()



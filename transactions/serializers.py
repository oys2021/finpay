from rest_framework import serializers
from transactions.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(source='user.id', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id',
            'transactionDate',
            'userId',
            'amountReceived',
            'receivingCurrency',
            'amount',
            'description'
        ]

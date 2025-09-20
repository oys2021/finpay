from rest_framework import serializers
from cards.models import VirtualCard

class VirtualCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualCard
        fields = "__all__"

from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cards.models import VirtualCard
from cards.serializers import *

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_active_card(request):
    try:
        card = VirtualCard.objects.filter(wallet__user=request.user, status="active").first()
        if not card:
            return Response({
                "status": 404,
                "message": "No active card found",
            }, status=404)

        serializer = VirtualCardSerializer(card)
        return Response({
            "status": 200,
            "message": "Retrieved active virtual card successfully",
            "data": serializer.data
        })
    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_virtual_card(request):
    try:
        wallet = request.user.wallet  # assuming user has a wallet
        data = request.data

        card = VirtualCard.objects.create(
            wallet=wallet,
            reference=data.get("reference", str(uuid.uuid4())),
            card_reference=data.get("card_reference", str(uuid.uuid4())),
            type=data.get("type", "virtual"),
            currency=data.get("currency", wallet.currency),
            holder_name=data.get("holder_name", request.user.get_full_name()),
            brand=data.get("brand", "Visa"),
            expiry_month=data.get("expiry_month", "12"),
            expiry_year=data.get("expiry_year", "25"),
            first_six=data.get("first_six", "111111"),
            last_four=data.get("last_four", "0000"),
            status="active",
            fees=data.get("fees", 0)
        )

        serializer = VirtualCardSerializer(card)
        return Response({
            "status": 201,
            "message": "Card created successfully",
            "data": serializer.data
        })
    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)



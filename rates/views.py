from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def exchange_rates(request):
    try:
        user_currency = getattr(request.user, "currency", "NGN")  

        rates = [
            {"currency": "USD", "buyPrice": "1,320", "sellPrice": "1,390"},
            {"currency": "EUR", "buyPrice": "1,255", "sellPrice": "1,755"},
            {"currency": "GBP", "buyPrice": "1,425", "sellPrice": "1,500"},
        ]

        return Response({
            "status": 200,
            "message": "Retrieved current exchange rates successfully",
            "data": {
                "currency": user_currency,
                "rates": rates
            }
        })
    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)

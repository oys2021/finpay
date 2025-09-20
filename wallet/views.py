from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from decimal import Decimal
from wallet.models import Account
from wallet.serializers import AccountSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_balances(request):
    try:
        wallet = request.user.wallet
        balances = wallet.balances.all()

        response_data = {}
        total = Decimal("0.00")

        for b in balances:
            currency_key = b.currency.lower()  
            response_data[currency_key] = str(b.balance)
            total += b.balance

        response_data["total"] = str(total)
        response_data["currency"] = "USD"  

        return Response({
            "status": 200,
            "message": "All balances retrieved successfully",
            "data": response_data
        }, status=200)

    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)
    



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_accounts(request):
    try:
        wallet = request.user.wallet
        accounts = wallet.accounts.all()  
        serializer = AccountSerializer(accounts, many=True)
        
        return Response({
            "status": 200,
            "message": "All balances retrieved successfully",
            "data": {
                "accounts": serializer.data
            }
        })
    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_account_detail(request, id):
    try:
        wallet = request.user.wallet

        # Filter account by ID and ensure it belongs to the user's wallet
        account = wallet.accounts.filter(id=id).first()
        if not account:
            return Response({
                "status": 404,
                "message": "Account not found"
            }, status=404)

        serializer = AccountSerializer(account)
        return Response({
            "status": 200,
            "message": "Retrieved account successfully",
            "data": serializer.data
        })

    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)
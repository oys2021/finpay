from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from decimal import Decimal
from accounts.models import Account
from accounts.serializers import AccountSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def user_accounts(request):
    try:
        wallet = request.user.wallet  

        if request.method == "GET":
            accounts = wallet.accounts.all()
            serializer = AccountSerializer(accounts, many=True)
            return Response({
                "status": 200,
                "message": "All accounts retrieved successfully",
                "data": {
                    "accounts": serializer.data
                }
            })

        elif request.method == "POST":
            serializer = AccountSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(wallet=wallet) 
                return Response({
                    "status": 201,
                    "message": "Bank account created successfully",
                    "data": serializer.data
                }, status=201)
            return Response({
                "status": 400,
                "message": serializer.errors
            }, status=400)

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
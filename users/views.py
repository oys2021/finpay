from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.serializers import RegisterSerializer,LoginSerializer,PasswordResetSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from decimal import Decimal

@api_view(["POST"])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.to_representation(user), status=status.HTTP_201_CREATED)
    return Response({"status": 400, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response({"status": 400, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def password_reset_view(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response({"status": 400, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def logout_view(request):
    from .serializers import LogoutSerializer
    serializer = LogoutSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            user = request.user if request.user.is_authenticated else None
            return Response({
                "status": 200,
                "message": "User logged out successfully",
                "data": {
                    "email": getattr(user, "email", None),
                    "name": getattr(user, "name", None),
                    "accountType": getattr(user, "accountType", None),
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": 400, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"status": 400, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



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
    


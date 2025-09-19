from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import RegisterSerializer,LoginSerializer,PasswordResetSerializer

@api_view(["POST"])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.save(), status=status.HTTP_201_CREATED)
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



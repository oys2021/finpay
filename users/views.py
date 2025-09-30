from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Q

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
    


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    try:
        serializer = CurrentUserSerializer(request.user)
        return Response({
            "status": 201,
            "message": "Retrieved currently logged-in user successfully",
            "data": serializer.data
        })
    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)
    


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_user_profile(request, id):
    try:
        user = User.objects.get(id=id)
        
        if request.user.id != user.id:
            return Response({
                "status": 403,
                "message": "You cannot edit another user's profile"
            }, status=403)

        data = request.data
        for field in ["first_name", "last_name", "email", "phone_number", 
                      "country", "tag", "occupation", "address", "dateOfBirth"]:
            if field in data:
                setattr(user, field, data[field])

        user.save()

        serializer = RegisterSerializer(user)  
        return Response({
            "status": 201,
            "message": "User edited successfully",
            "data": serializer.data["data"]["user"] 
        })

    except User.DoesNotExist:
        return Response({
            "status": 400,
            "message": "User not found"
        }, status=400)
    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)
    



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_beneficiary(request, id):
    try:
        user = User.objects.get(id=id)
        
        if request.user.id != user.id:
            return Response({
                "status": 403,
                "message": "You cannot add a beneficiary to another user's account"
            }, status=403)

        data = request.data
        beneficiary = Beneficiary.objects.create(
            user=user,
            name=data.get("name"),
            bankName=data.get("bankName"),
            accountNumber=data.get("accountNumber"),
            accountType=data.get("accountType"),
            isDefault=data.get("isDefault", False),
            country=data.get("country")
        )

        serializer = BeneficiarySerializer(beneficiary)
        return Response({
            "status": 201,
            "message": "Beneficiary successfully created",
            "data": serializer.data
        })

    except User.DoesNotExist:
        return Response({
            "status": 400,
            "message": "User not found"
        }, status=400)
    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)
    


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_beneficiaries(request):
    try:
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))
        search = request.query_params.get("search", "")

        # Filter beneficiaries of the authenticated user
        beneficiaries_qs = Beneficiary.objects.filter(user=request.user)

        # Apply search if provided
        if search:
            beneficiaries_qs = beneficiaries_qs.filter(
                Q(name__icontains=search) |
                Q(bankName__icontains=search) |
                Q(accountNumber__icontains=search) |
                Q(accountType__icontains=search) |
                Q(country__icontains=search)
            )

        total = beneficiaries_qs.count()

        paginator = Paginator(beneficiaries_qs, size)
        current_page = page + 1
        beneficiaries_page = paginator.get_page(current_page)

        serializer = BeneficiarySerializer(beneficiaries_page, many=True)

        return Response({
            "status": 201,
            "message": "Retrieved all searched and paginated beneficiaries successfully",
            "page": page,
            "size": size,
            "total": total,
            "data": serializer.data
        })

    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)



@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def beneficiary_detail(request, id):
    try:
        beneficiary = Beneficiary.objects.get(id=id, user=request.user)
    except Beneficiary.DoesNotExist:
        return Response({
            "status": 400,
            "message": "Beneficiary not found"
        }, status=400)

    if request.method == "GET":
        serializer = BeneficiarySerializer(beneficiary)
        return Response({
            "status": 200,
            "message": "Retrieved a single beneficiary successfully",
            "data": serializer.data
        })

    elif request.method == "DELETE":
        beneficiary.delete()
        return Response({
            "status": 200,
            "message": "Beneficiary deleted successfully",
            "data": {}
        })
    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def activate_2fa(request):
    data = request.data
    phone_number = data.get("phoneNumber")
    method_type = data.get("type")  

    if not phone_number or not method_type:
        return Response({
            "status": 400,
            "message": "phoneNumber and type are required"
        }, status=400)


    return Response({
        "status": 200,
        "message": "You have successfully activated 2FA",
        "data": {}
    })


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_verification(request):
    user = request.user

    redirect_link = f"https://verification.example.com/start?user_id={user.id}"

    return Response({
        "status": 201,
        "message": "Verification successfully created",
        "data": {
            "redirectLink": redirect_link
        }
    })






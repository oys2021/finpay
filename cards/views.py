from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cards.models import VirtualCard
from cards.serializers import *
import uuid
from django.core.paginator import Paginator


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_active_card(request):
#     try:
#         card = VirtualCard.objects.filter(wallet__user=request.user, status="active").first()
#         if not card:
#             return Response({
#                 "status": 404,
#                 "message": "No active card found",
#             }, status=404)

#         serializer = VirtualCardSerializer(card)
#         return Response({
#             "status": 200,
#             "message": "Retrieved active virtual card successfully",
#             "data": serializer.data
#         })
#     except Exception as e:
#         return Response({
#             "status": 400,
#             "message": str(e)
#         }, status=400)
    


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def virtual_cards(request):
    if request.method == "POST":
        try:
            data = request.data
            wallet_id = data.get("walletId")
            if not wallet_id:
                return Response({
                    "status": 400,
                    "message": "walletId is required"
                }, status=400)

            
            # if str(request.user.wallet.id) != str(wallet_id):
            #     return Response({
            #         "status": 403,
            #         "message": "You cannot create a card for this wallet"
            #     }, status=403)

            wallet = request.user.wallet

            card = VirtualCard.objects.create(
                wallet=wallet,
                reference=data.get("reference", str(uuid.uuid4())),
                card_reference=data.get("card_reference", str(uuid.uuid4())),
                type=data.get("type", "virtual"),
                holder_name=data.get("name", request.user.get_full_name()),
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

    elif request.method == "GET":
        try:
            page = int(request.query_params.get("page", 0))
            size = int(request.query_params.get("size", 10))

            cards_qs = VirtualCard.objects.filter(wallet=request.user.wallet)
            total = cards_qs.count()

            paginator = Paginator(cards_qs, size)
            current_page = page + 1 
            cards_page = paginator.get_page(current_page)

            serializer = VirtualCardSerializer(cards_page, many=True)
            return Response({
                "status": 200,
                "message": "Virtual cards retrieved successfully",
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

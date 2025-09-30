from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from decimal import Decimal
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError


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
def wallet_balance(request):
    try:
        user_wallet = request.user.wallet

        currency = request.query_params.get("currency")

        if currency:
            balance_obj = user_wallet.balances.filter(currency=currency).first()
            if not balance_obj:
                return Response({
                    "status": 400,
                    "message": f"No balance found for currency '{currency}'"
                }, status=400)

            balance_data = {
                "balance": f"{balance_obj.balance:,}",  
                "currency": balance_obj.currency
            }
        else:
            balance_obj = user_wallet.balances.first()
            if not balance_obj:
                return Response({
                    "status": 400,
                    "message": "No balances found in your wallet"
                }, status=400)

            balance_data = {
                "balance": f"{balance_obj.balance:,}",
                "currency": balance_obj.currency
            }

        return Response({
            "status": 200,
            "message": "Balance retrieved successfully",
            "data": balance_data
        })

    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)
    



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def wallet_balance(request):
    try:
        currency = request.query_params.get("currency")
        wallet = request.user.wallet

        if not currency:
            return Response({
                "status": 400,
                "message": "currency query parameter is required"
            }, status=400)

        
        balance_obj = wallet.balances.filter(currency__iexact=currency).first()
        if not balance_obj:
            return Response({
                "status": 400,
                "message": f"No balance found for currency: {currency}"
            }, status=400)

        return Response({
            "status": 200,
            "message": "Balance retrieved successfully",
            "data": {
                "balance": f"{balance_obj.balance:,.2f}",  
                "currency": balance_obj.currency
            }
        })

    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)

    





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def wallet_statements(request):
    try:
        start_date_str = request.query_params.get("startDate")
        end_date_str = request.query_params.get("endDate")

        if not start_date_str or not end_date_str:
            return Response({
                "status": 400,
                "message": "Both startDate and endDate are required"
            }, status=400)

        
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        if not start_date or not end_date:
            return Response({
                "status": 400,
                "message": "Invalid date format. Use YYYY-MM-DD."
            }, status=400)

        if start_date > end_date:
            return Response({
                "status": 400,
                "message": "startDate cannot be after endDate"
            }, status=400)

        statement_link = f"https://example.com/statements/{uuid.uuid4()}.pdf"

        return Response({
            "status": 200,
            "message": "Statement retrieved successfully",
            "data": {
                "link": statement_link,
                "startDate": start_date_str,
                "endDate": end_date_str
            }
        })

    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)
    

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import ReceivingAccount  
# from .serializers import ReceivingAccountSerializer

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def receiving_account_detail(request, id=None):
#     try:
#         currency = request.query_params.get("currency")
#         wallet = request.user.wallet

#         if id:  # get a single account by ID
#             account = ReceivingAccount.objects.filter(wallet=wallet, id=id)
#             if currency:
#                 account = account.filter(currency__iexact=currency)
#             account = account.first()
#             if not account:
#                 return Response({
#                     "status": 400,
#                     "message": "Account not found"
#                 }, status=400)
#             serializer = ReceivingAccountSerializer(account)
#             data = serializer.data
#         else:  # get all accounts
#             accounts = ReceivingAccount.objects.filter(wallet=wallet)
#             if currency:
#                 accounts = accounts.filter(currency__iexact=currency)
#             serializer = ReceivingAccountSerializer(accounts, many=True)
#             data = serializer.data

#         return Response({
#             "status": 200,
#             "message": "Account(s) retrieved successfully",
#             "data": data
#         })

#     except Exception as e:
#         return Response({
#             "status": 400,
#             "message": str(e)
#         }, status=400)



# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from django.db.models import Sum
# from .models import Transaction  # assuming you have a Transaction model

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def income_expense_summary(request):
#     try:
#         user = request.user

#         income_total = Transaction.objects.filter(user=user, type="income").aggregate(total=Sum("amount"))["total"] or 0
#         expense_total = Transaction.objects.filter(user=user, type="expense").aggregate(total=Sum("amount"))["total"] or 0

#         return Response({
#             "status": 200,
#             "message": "All incomes and expenses retrieved successfully",
#             "data": {
#                 "income": float(income_total),
#                 "expense": float(expense_total)
#             }
#         })

#     except Exception as e:
#         return Response({
#             "status": 400,
#             "message": str(e)
#         }, status=400)


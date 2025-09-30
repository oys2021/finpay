from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from decimal import Decimal
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
import uuid
from wallet.serializers import *
from rest_framework import status
from django.db.models import Sum
from transactions.models import Transaction
from wallet.models import WalletBalance
from django.utils.timezone import now


EXCHANGE_RATES = {
    "USD": {"EUR": 0.9, "GHS": 12.5},
    "EUR": {"USD": 1.1, "GHS": 14.0},
    "GHS": {"USD": 0.08, "EUR": 0.07},
}


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
        wallet = request.user.wallet
        currency = request.query_params.get("currency")

        if currency:
            balance_obj = wallet.balances.filter(currency__iexact=currency).first()
            if not balance_obj:
                return Response({
                    "status": 400,
                    "message": f"No balance found for currency '{currency}'"
                }, status=400)

            return Response({
                "status": 200,
                "message": "Balance retrieved successfully",
                "data": {
                    "balance": f"{balance_obj.balance:,.2f}",
                    "currency": balance_obj.currency
                }
            })

    
        balances = wallet.balances.all()
        if not balances.exists():
            return Response({
                "status": 400,
                "message": "No balances found in your wallet"
            }, status=400)

        balances_data = [
            {
                "balance": f"{bal.balance:,.2f}",
                "currency": bal.currency
            }
            for bal in balances
        ]

        return Response({
            "status": 200,
            "message": "Balances retrieved successfully",
            "data": balances_data
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
 



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_wallet_accounts(request, id=None):
    try:
        balances = WalletBalance.objects.filter(wallet=request.user.wallet)

        if id:
            balance = balances.get(id=id)
            serializer = WalletBalanceSerializer(balance)
            return Response({
                "status": 200,
                "message": "Balance retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        
        currency = request.query_params.get("currency")
        if currency:
            balances = balances.filter(currency=currency)

        serializer = WalletBalanceSerializer(balances, many=True)
        return Response({
            "status": 200,
            "message": "Balances retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    except WalletBalance.DoesNotExist:
        return Response({
            "status": 400,
            "message": "Account not found"
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def wallet_expenses_incomes(request):
    try:
        wallet = request.user.wallet

        income_sum = wallet.transactions.filter(transaction_type="INCOME").aggregate(total=Sum("amount"))["total"] or 0
        expense_sum = wallet.transactions.filter(transaction_type="EXPENSE").aggregate(total=Sum("amount"))["total"] or 0

        return Response({
            "status": 200,
            "message": "All incomes and expenses retrieved successfully",
            "data": {
                "income": float(income_sum),
                "expense": float(expense_sum)
            }
        })

    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_funds(request):
    try:
        wallet = request.user.wallet
        data = request.data

        amount = Decimal(data.get("amount", 0))
        currency = data.get("currency")
        receiving_currency = data.get("recievingCurrency")
        account_type = data.get("accountType")
        account_id = data.get("accountID")
        description = data.get("description")
        agent_phone = data.get("agentPhoneNumber")

        
        if amount <= 0:
            return Response({"status": 400, "message": "Amount must be greater than 0"}, status=400)

        
        balance_obj = wallet.balances.filter(currency__iexact=currency).first()
        if not balance_obj:
            balance_obj, created = wallet.balances.get_or_create(currency__iexact=currency, defaults={"balance": Decimal("0.00")})

        
        # balance_obj, created = wallet.balances.get_or_create(currency__iexact=currency, defaults={"balance": Decimal("0.00")})

        if balance_obj.balance < amount:
            return Response({"status": 400, "message": "Insufficient funds"}, status=400)


        amount_received = amount  

        
        balance_obj.balance -= amount
        balance_obj.save()

        transaction = Transaction.objects.create(
            wallet=wallet,
            transaction_type="TRANSFER",
            amount=amount,
            currency=currency,
            receiving_currency=receiving_currency,
            account_type=account_type,
            account_id=account_id,
            agent_phone_number=agent_phone,
            description=description
        )

        return Response({
            "status": 201,
            "message": "You have successfully sent your fund",
            "data": {
                "id": transaction.id,
                "transactionDate": transaction.created_at,
                "userId": request.user.id,
                "amountRecieved": float(amount_received),
                "recievingCurrency": receiving_currency,
                "amount": float(amount),
                "currency": currency,
                "accountType": account_type,
                "accountID": account_id,
                "agentPhoneNumber": agent_phone,
                "description": description
            }
        }, status=201)

    except Exception as e:
        return Response({"status": 400, "message": str(e)}, status=400)
    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def convert_currency(request):
    try:
        wallet = request.user.wallet
        data = request.data

        amount = Decimal(data.get("amount", 0))
        source_currency = data.get("currency")
        target_currency = data.get("targetCurrency")

        if amount <= 0:
            return Response({"status": 400, "message": "Amount must be greater than 0"}, status=400)
        if not target_currency:
            return Response({"status": 400, "message": "targetCurrency is required"}, status=400)

        source_balance = wallet.balances.filter(currency__iexact=source_currency).first()
        if not source_balance or source_balance.balance < amount:
            return Response({"status": 400, "message": f"Insufficient {source_currency} balance"}, status=400)

        rate = EXCHANGE_RATES.get(source_currency, {}).get(target_currency)
        if not rate:
            return Response({"status": 400, "message": f"No conversion rate from {source_currency} to {target_currency}"}, status=400)

        converted_amount = amount * Decimal(rate)

        source_balance.balance -= amount
        source_balance.save()

        target_balance, _ = wallet.balances.get_or_create(currency=target_currency, defaults={"balance": 0})
        target_balance.balance += converted_amount
        target_balance.save()

        transaction = Transaction.objects.create(
            wallet=wallet,
            transaction_type="CONVERSION",
            amount=amount,
            currency=source_currency,
            target_currency=target_currency,
            converted_amount=converted_amount
        )

        return Response({
            "status": 201,
            "message": "You have successfully converted your fund",
            "data": {
                "id": transaction.id,
                "conversionDate": transaction.created_at,
                "currency": source_currency,
                "targetCurrency": target_currency,
                "amount": float(amount),
                "convertedAmount": float(converted_amount)
            }
        }, status=201)

    except Exception as e:
        return Response({"status": 400, "message": str(e)}, status=400)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def deposit_wallet(request):
    user = request.user
    amount = request.data.get("amount")
    payment_method = request.data.get("paymentMethod", "mobile_money")
    currency = request.data.get("currency", "GHS")

    if not amount:
        return Response({
            "status": 400,
            "message": "Amount is required."
        }, status=status.HTTP_400_BAD_REQUEST)

    transaction = Transaction.objects.create(
        user=user,
        transaction_id=str(uuid.uuid4()),
        amount=amount,
        currency=currency,
        payment_method=payment_method,
        status="pending"
    )

    

    return Response({
        "status": 201,
        "message": "Deposit initiated successfully. Awaiting confirmation.",
        "data": {
            "transactionId": transaction.transaction_id,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "paymentMethod": transaction.payment_method,
            "status": transaction.status
        }
    }, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def withdraw_wallet(request):
    user = request.user
    data = request.data

    amount = data.get("amount")
    account_type = data.get("accountType")
    account_id = data.get("accountID")
    currency = data.get("currency", "GHS")
    receiving_currency = data.get("recievingCurrency", "GHS")
    description = data.get("description", "")
    agent_phone = data.get("agentPhoneNumber", "")

    # Validate required fields
    if not amount or not account_type or not account_id:
        return Response({
            "status": 400,
            "message": "Amount, accountType, and accountID are required."
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        return Response({
            "status": 400,
            "message": "Wallet not found."
        }, status=status.HTTP_400_BAD_REQUEST)

    if wallet.balance < float(amount):
        return Response({
            "status": 400,
            "message": "Insufficient balance for withdrawal."
        }, status=status.HTTP_400_BAD_REQUEST)

    # Deduct balance immediately
    wallet.balance -= float(amount)
    wallet.save()

    # Create withdrawal transaction
    transaction = Transaction.objects.create(
        user=user,
        transaction_id=str(uuid.uuid4()),
        amount=amount,
        currency=currency,
        payment_method="withdraw",
        status="successful",  # or "pending" if third-party confirmation needed
        description=description,
        account_id=account_id,
        account_type=account_type,
        agent_phone=agent_phone,
        receiving_currency=receiving_currency,
    )

    return Response({
        "status": 201,
        "message": "You have successfully withdrawn your fund",
        "data": {
            "id": transaction.transaction_id,
            "transactionDate": transaction.created_at,
            "userId": transaction.user.id,
            "amountRecieved": transaction.amount,
            "recievingCurrency": transaction.receiving_currency,
            "amount": transaction.amount,
            "accountType": transaction.account_type,
            "accountID": transaction.account_id,
            "description": transaction.description,
        }
    }, status=status.HTTP_201_CREATED)
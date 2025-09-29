from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Transaction
from .serializers import TransactionSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_transactions(request):
    try:
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))
        search = request.query_params.get("search")
        filter_by = request.query_params.get("filterBy")

        user = request.user
        transactions_qs = Transaction.objects.filter(user=user).order_by("-transactionDate")

        # Apply search
        if search:
            transactions_qs = transactions_qs.filter(
                Q(description__icontains=search) |
                Q(amount__icontains=search) |
                Q(receivingCurrency__icontains=search) |
                Q(amountReceived__icontains=search)
            ).distinct()

       
        if filter_by:
            
            import json
            try:
                filter_dict = json.loads(filter_by)
                transactions_qs = transactions_qs.filter(**filter_dict)
            except Exception:
                return Response({
                    "status": 400,
                    "message": "Invalid filterBy parameter"
                }, status=400)

        total = transactions_qs.count()

        # Pagination
        paginator = Paginator(transactions_qs, size)
        current_page = page + 1
        transactions_page = paginator.get_page(current_page)

        serializer = TransactionSerializer(transactions_page, many=True)

        # Determine message
        if search and filter_by:
            message = "Retrieved all searched, filtered and paginated transactions successfully"
        elif search:
            message = "Retrieved all searched and paginated transactions successfully"
        elif filter_by:
            message = "Retrieved all filtered and paginated transactions successfully"
        else:
            message = "Retrieved all paginated transactions successfully"

        return Response({
            "status": 201,
            "message": message,
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def transaction_detail(request, id):
    try:
        user = request.user
        transaction = Transaction.objects.filter(id=id, user=user).first()

        if not transaction:
            return Response({
                "status": 400,
                "message": "Transaction not found"
            }, status=400)

        serializer = TransactionSerializer(transaction)

        return Response({
            "status": 201,
            "message": "Retrieved a single transaction successfully",
            "data": serializer.data
        })

    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)
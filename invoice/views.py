from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from invoice.models import Invoice, InvoiceItem
from invoice.serializers import InvoiceSerializer
import uuid

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def invoice_summary(request):
    try:
        invoices = request.user.invoices.all()

        summary = {
            "due": invoices.filter(status="due").count(),
            "overdue": invoices.filter(status="overdue").count(),
            "pending": invoices.filter(status="pending").count(),
        }

        return Response({
            "status": 200,
            "message": "Retrieved invoices summaries successfully",
            "data": {"invoices": summary}
        })

    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_invoice(request):
    try:
        data = request.data
        items_data = data.get("items", [])

        invoice = Invoice.objects.create(
            user=request.user,
            currency=data.get("currency", "USD"),
            issue_date=data.get("issueDate"),
            due_date=data.get("dueDate"),
            status="due"
        )

        for item in items_data:
            InvoiceItem.objects.create(
                invoice=invoice,
                description=item["description"],
                quantity=item["quantity"],
                amount=item["amount"]
            )

        serializer = InvoiceSerializer(invoice)
        return Response({
            "status": 201,
            "message": "Invoice created successfully",
            "data": serializer.data
        })
    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)



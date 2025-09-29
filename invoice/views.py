from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from invoice.models import Invoice, InvoiceItem
from invoice.serializers import InvoiceSerializer
import uuid
from django.db.models import Q

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
    

@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def invoices(request):
    if request.method == "POST":
        try:
            data = request.data
            items_data = data.get("items", [])

            user = request.user  

            invoice = Invoice.objects.create(
                user=user,
                currency=data.get("currency", "USD"),
                issue_date=data.get("issueDate"),
                due_date=data.get("dueDate"),
                status=data.get("status", "draft")
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

    elif request.method == "GET":
        try:
            page = int(request.query_params.get("page", 0))
            size = int(request.query_params.get("size", 10))
            offset = page * size

            invoices_qs = Invoice.objects.filter(user=request.user)

            status = request.query_params.get("status")
            if status:
                invoices_qs = invoices_qs.filter(status=status)

            filter_params = request.query_params.get("filter")
            if filter_params:
                for key, value in request.query_params.items():
                    if key.startswith("filter[") and key.endswith("]"):
                        field_name = key[7:-1]
                        invoices_qs = invoices_qs.filter(**{f"customer__{field_name}__icontains": value})

            terms = request.query_params.get("terms")
            if terms:
                invoices_qs = invoices_qs.filter(
                    Q(customer__name__icontains=terms) |
                    Q(customer__email__icontains=terms) |
                    Q(items__description__icontains=terms)
                ).distinct()

            total = invoices_qs.count()
            invoices_qs = invoices_qs[offset: offset + size]

            serializer = InvoiceSerializer(invoices_qs, many=True)

            return Response({
                "status": 200,
                "message": "Invoices retrieved successfully",
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
        

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_invoice(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id, user=request.user)
        invoice.delete()
        return Response({
            "status": 200,
            "message": "Invoice deleted successfully",
            "data": {}
        })
    except Invoice.DoesNotExist:
        return Response({
            "status": 400,
            "message": "Invoice not found or you do not have permission to delete it."
        }, status=400)
    except Exception as e:
        return Response({
            "status": 400,
            "message": str(e)
        }, status=400)

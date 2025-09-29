from django.urls import path
from .views import *

urlpatterns = [
    path("", invoices, name="invoices"),
    path("summary", invoice_summary, name="invoice-summary"),
    path("invoices/<uuid:invoice_id>/", delete_invoice, name="delete-invoice"),
]



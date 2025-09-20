from django.urls import path
from .views import *

urlpatterns = [
    path("", create_invoice, name="create-invoice"),
    path("summary", invoice_summary, name="invoice-summary"),
]


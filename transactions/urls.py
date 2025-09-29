from django.urls import path
from transactions.views import *

urlpatterns = [
    path("", list_transactions, name="exchange-rates"),
    path("transactions/<uuid:id>/", transaction_detail, name="transaction-detail"),
]

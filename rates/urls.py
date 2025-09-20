from django.urls import path
from .views import exchange_rates

urlpatterns = [
    path("rates", exchange_rates, name="exchange-rates"),
]

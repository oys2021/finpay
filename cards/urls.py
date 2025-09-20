from django.urls import path
from .views import get_active_card, create_virtual_card

urlpatterns = [
    path("", get_active_card, name="get-active-card"),
    path("", create_virtual_card, name="create-virtual-card"),
]

from django.urls import path
from .views import  virtual_cards

urlpatterns = [
    # path("", get_active_card, name="get-active-card"),
    path("", virtual_cards, name="create-virtual-card"),
]

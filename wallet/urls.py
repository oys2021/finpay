from django.urls import path
from .views import *


urlpatterns = [ 
    #wallets balance and create an account api or section
    path("users/balances", get_user_balances, name="user-balances"),
    
]

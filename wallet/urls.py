from django.urls import path
from .views import *


urlpatterns = [ 
    #wallets balance and create an account api or section
    path("users/balances", get_user_balances, name="user-balances"),
    path("accounts", user_accounts, name="user-accounts"),
     path("accounts/<uuid:id>", user_account_detail, name="user-account-detail"),
]

from django.urls import path
from .views import *


urlpatterns = [ 
    path("users/balances", get_user_balances, name="user-balances"),
    path("balance", wallet_balance, name="current-balances"),
    path("statements", wallet_statements, name="wallet-statements"),
    path("accounts/", get_wallet_accounts, name="wallet-accounts"),
    path("accounts/<int:id>", get_wallet_accounts, name="wallet-account-detail"),
    path("expenses-incomes", wallet_expenses_incomes, name="wallet-expenses-incomes"),
    path("send", send_funds, name="wallet-send"),
    path("convert", convert_currency, name="wallet-convert"),
    path("deposit", deposit_wallet, name="deposit-wallet"),
    path("withdraw", withdraw_wallet, name="withdraw-wallet"),
]

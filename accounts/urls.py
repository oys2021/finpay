from django.urls import path
from accounts.views import *

urlpatterns=[
    path("", user_accounts, name="user-accounts"),
    path("accounts/<uuid:id>", user_account_detail, name="user-account-detail")
]
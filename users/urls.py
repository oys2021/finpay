from django.urls import path
from users.views import *

urlpatterns=[
    path("auth/register", register_view, name="register"),
    path("auth/login", login_view, name="login"),
    path("auth/password/reset", password_reset_view, name="password_reset"),
    path("auth/logout", logout_view, name="logout"),
    path("users/balances", get_user_balances, name="user-balances"),
    path('currentUser', current_user, name='current-user'),
    path('users/<str:id>', edit_user_profile, name='edit-user-profile'),
    path('users/<str:id>/beneficiaries', add_beneficiary, name='add-beneficiary'),
    path("beneficiaries", list_beneficiaries, name="list-beneficiaries"),
    path("beneficiaries/<str:id>", beneficiary_detail, name="beneficiary-detail"),
    path("users/2fa", activate_2fa, name="activate-2fa"),
    path("verification", create_verification, name="create-verification")



]
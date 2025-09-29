from django.urls import path
from users.views import *

urlpatterns=[
    path("auth/register", register_view, name="register"),
    path("auth/login", login_view, name="login"),
    path("auth/password/reset", password_reset_view, name="password_reset"),
    path("auth/logout", logout_view, name="logout"),
    path("users/balances", get_user_balances, name="user-balances"),

]
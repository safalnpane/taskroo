""" Users-related URLs"""
from django.urls import path

from .api import (
    login_view,
    signup_view,
    password_reset_request,
    confirm_otp,
    password_reset_confirm,
)


urlpatterns = [
    path("login", login_view, name="login"),
    path("register", signup_view, name="register"),
    path("passwordreset/<str:email>", password_reset_request, name="password_reset"),
    path("confirm/<str:otp_code>", confirm_otp, name="confirm_otp"),
    path(
        "passwordresetconfirm/<str:otp_code>",
        password_reset_confirm,
        name="password_reset_confirm",
    ),
]

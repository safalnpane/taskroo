import pytest
from mixer.backend.django import mixer
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from ..api import confirm_otp, password_reset_confirm
from ..models import OTP
from ..utils import OTPAction

pytestmark = pytest.mark.django_db


def test_login_success(client):
    """
    Login with username and password
    should return a JSON object with "user", "token", and
    "login_message"
    """
    test_user_info = {"username": "safal", "password": "safal1234"}
    user = get_user_model().objects.create_user(**test_user_info)
    resp = client.post(reverse("login"), test_user_info)
    assert resp.status_code == 200, "Should return 200"
    assert "user" in resp.data, "Should return user details"
    assert resp.data["user"]["username"] == user.username, "Should match user"
    assert "token" in resp.data, "Should return token"
    assert "login_message" in resp.data, "Should return login message"


def test_registration_success(client):
    """
    User registration should return "user", and "token"
    """
    test_user_info = {
        "username": "safal",
        "password": "safal12345",
        "email": "safal@gmail.com",
        "first_name": "Safal",
        "last_name": "Neupane",
    }
    resp = client.post(reverse("register"), test_user_info)
    assert resp.status_code == 201, "Should return 201"
    assert "user" in resp.data, "Should return user details"
    assert "token" in resp.data, "Should return token"


def test_registration_email_duplication(client):
    """ Registraion with duplicate email returns 400 bad request """
    test_user_info = {
        "username": "safal",
        "password": "safal12345",
        "email": "safal@gmail.com",
        "first_name": "Safal",
        "last_name": "Neupane",
    }
    _ = mixer.blend(get_user_model(), email=test_user_info["email"])
    resp = client.post(reverse("register"), test_user_info)
    assert resp.status_code == 400, "Should return 400"


def test_confirm_otp_registration():
    """
    OTP confirmation should return appropriate message
    and should verify user in successful confirmation
    """
    user = mixer.blend(get_user_model(), email="safal@gmail.com")
    otp = OTP.objects.create(user=user, otp_for=OTPAction.REGISTRATION)
    req = APIRequestFactory().get("/")
    force_authenticate(req, user=user)

    resp = confirm_otp(req, otp.code)
    assert resp.status_code == 200, "Should return 200"
    assert "message" in resp.data, "Should return message"
    assert (
        resp.data["message"] == "Thank you for confirming your account"
    ), "Should return proper message"

    # User model should have is_verified to True
    assert user.is_verified, "is_verified should be set to True"


def test_confirm_otp_password_reset():
    """
    Password rest OTP confirmation should return appropriate
    message and redirect user to password reset link if successful.
    """
    user = mixer.blend(get_user_model(), email="safal@gmail.com")
    otp = OTP.objects.create(user=user, otp_for=OTPAction.PASSWORD_RESET)
    req = APIRequestFactory().get("/")
    force_authenticate(req, user=user)

    resp = confirm_otp(req, otp.code)
    assert resp.status_code == 302, "Should return 302"
    assert (
        "passwordresetconfirm" in resp.url
    ), "Should redirect to password reset confirm"


def test_confirm_otp_password_reset_confirm():
    """
    If OTP is valid and both password fields matched,
    password should be reset and appropriate message should be
    returned.
    """
    user = mixer.blend(get_user_model(), email="safal@gmail.com")
    otp = OTP.objects.create(user=user, otp_for=OTPAction.PASSWORD_RESET)
    req = APIRequestFactory().post(
        "/", {"password1": "safal12345", "password2": "safal12345"}
    )
    force_authenticate(req, user=user)

    resp = password_reset_confirm(req, otp.code)
    assert resp.status_code == 200, "Should return 200"
    assert "message" in resp.data, "Should return message"
    assert (
        resp.data["message"] == "Your password has been updated"
    ), "should return proper message"

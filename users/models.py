""" User-realted models """
import secrets
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from .utils import OTPAction


class CustomUser(AbstractUser):
    """
    Extending some user attributes
    """
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class OTP(models.Model):
    """
    One-Time-Password (OTP) are to be used for critical actions such as confirming registration
    and password reset action. Verification code is auto generated for each instance and
    contains a 6 character long random string.

    After user submit the valid verification code received via email, the view is responsible for
    deleting that particulr row.
    """
    code = models.CharField(max_length=6, default=secrets.token_urlsafe(4))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="otp")
    otp_for = models.IntegerField(choices=OTPAction.choices())

    def __str__(self):
        """Return username"""
        return self.user.__str__()

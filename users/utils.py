"""Utis for users"""
from enum import IntEnum


class OTPAction(IntEnum):
    """Enum representing different OTP actions"""

    REGISTRATION = 1
    PASSWORD_RESET = 2

    @classmethod
    def choices(cls):
        """Choices for model field"""
        return [(key.value, key.name) for key in cls]

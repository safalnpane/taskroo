import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from ..serializers import (
    LoginSerializer,
    UserSerializer,
    RegisterSerializer,
    PasswordResetSerializer,
)

pytestmark = pytest.mark.django_db


class TestLoginSerializer:
    def test_serializer_validate(self):
        valid_user_info = {"username": "safal", "password": "safal12345"}
        user = get_user_model().objects.create_user(**valid_user_info)  # type: ignore
        serializer = LoginSerializer(data=valid_user_info)  # type: ignore

        assert serializer.is_valid(raise_exception=True), "Should return True"
        assert serializer.validated_data == user, "Should return user instance"
        assert serializer.errors == {}, "Should not return any errors"

    def test_serializer_invalid(self):
        invalid_user_info = {"username": "safal", "password": "safal12345"}
        serializer = LoginSerializer(data=invalid_user_info)  # type: ignore

        assert not serializer.is_valid(), "Should return False"
        assert (
            "non_field_errors" in serializer.errors
        ), "Should complain about invalid creds"


class TestUserSerializer:
    def test_serializer_validate(self):
        user = mixer.blend(get_user_model())
        serializer = UserSerializer(user)
        validated_data = serializer.data

        assert "id" in validated_data, "Should include users id"
        assert "username" in validated_data, "Should include username"
        assert "first_name" in validated_data, "Should include users first_name"
        assert "last_name" in validated_data, "Should include users last_name"


class TestRegisterSerializer:
    @classmethod
    def setup_class(self):
        self.register_data = {
            "username": "safal",
            "password": "safal12345",
            "email": "safal@gmail.com",
            "project": "ASEEP",
            "school_name": "Aspeed School",
            "first_name": "Safal",
            "last_name": "Neupane",
            "phone": "0987654321",
        }

    def test_serializer_validate(self):
        serializer = RegisterSerializer(data=self.register_data)  # type: ignore

        assert serializer.is_valid(raise_exception=True), "Should return True"
        validated_data = serializer.validated_data
        user = get_user_model().objects.get(username="safal")
        assert validated_data == user, "Should return user instance"
        assert serializer.errors == {}, "Should not return any errors"

    def test_serializer_email_reused(self):
        """ValidationError should be raised for email duplication"""
        _ = get_user_model().objects.create_user(  # type: ignore
            username="abc", password="12345678", email="safal@gmail.com"
        )
        serializer = RegisterSerializer(data=self.register_data)  # type: ignore
        assert not serializer.is_valid(), "Should return False"
        assert "non_field_errors" in serializer.errors, "Should return an error"


def test_password_reset_serializer():
    password_info = {"password1": "safal12345", "password2": "safal12345"}
    serializer = PasswordResetSerializer(data=password_info)  # type: ignore
    assert serializer.is_valid(), "Should return True"
    assert serializer.errors == {}, "Should not return an error"


def test_password_reset_serializer_invalid():
    password_info = {"password1": "safal12345", "password2": "safal1234"}
    serializer = PasswordResetSerializer(data=password_info)  # type: ignore
    assert not serializer.is_valid(), "Should return False"
    assert "non_field_errors" in serializer.errors, "Should retrun an error"

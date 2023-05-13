""" Serializers for users """
#pylint: disable=W0223
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """ Username and Password for login """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentails")


class UserSerializer(serializers.Serializer):
    """ Few users details as a profile """
    id = serializers.CharField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    """ Basic user details on registration """
    username = serializers.CharField()
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        """
        Check if email already exists
        """
        user_model = get_user_model()
        try:
            _ = user_model.objects.get(email=attrs["email"])
            raise serializers.ValidationError("Email with this user already exists.")
        except user_model.DoesNotExist:
            pass

        # Create new user instance
        try:
            new_user = get_user_model().objects.create_user(**attrs)  # type: ignore
            return new_user
        except Exception as error:
            raise serializers.ValidationError(error)


class PasswordResetSerializer(serializers.Serializer):
    """ Password confirmation for password reset """
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        if attrs["password1"] == attrs["password2"]:
            return attrs["password1"]
        raise serializers.ValidationError("Password did not matched. Try again.")

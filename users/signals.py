"""Contains receiver for various signals dispatched from users app"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import OTP
from .utils import OTPAction


@receiver(post_save, sender=OTP)
def send_registration_confirmation_email(**kwargs):
    """
    Send email along with the OTP for registration confirmation
    """
    instance: OTP = kwargs["instance"]
    if instance.otp_for == OTPAction.REGISTRATION:
        send_registration_email(instance)
    if instance.otp_for == OTPAction.PASSWORD_RESET:
        send_password_reset_email(instance)


def send_password_reset_email(instance: OTP) -> None:
    """
    Send email along with the OTP for password reset request
    """
    send_mail(
        subject="Password reset confirmation",
        message=f"""Dear {instance.user.username},
        Please confirm your password reset request by using this OTP: {instance.code}
        
        Thanks,
        Taskroo Team""",
        from_email="admin@taskroo.com",
        recipient_list=[instance.user.email],
    )


def send_registration_email(instance: OTP) -> None:
    """
    Send email with given OTP
    """
    send_mail(
        subject="Confirm your Registration",
        message=f"""Dear {instance.user.username},
        Please complete your registration by confirming this OTP: {instance.code}
        
        Thanks,
        Taskroo Team""",
        from_email="admin@taskroo.com",
        recipient_list=[instance.user.email],
    )

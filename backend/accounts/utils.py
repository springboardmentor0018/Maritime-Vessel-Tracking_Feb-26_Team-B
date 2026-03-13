"""
Accounts utilities — OTP generation and email sending
"""
from django.core.mail import send_mail
from django.conf import settings
from .models import OTPCode


def create_and_send_otp(user):
    """
    Generate a new OTP for the user and send it via email.
    In development (console email backend), the OTP will be printed to stdout.
    Returns the OTP code string.
    """
    # Invalidate any previous unused OTPs
    OTPCode.objects.filter(user=user, is_used=False).update(is_used=True)

    # Create new OTP
    code = OTPCode.generate_code()
    OTPCode.objects.create(user=user, code=code)

    # Send email
    subject = 'Vessel Tracker — Email Verification OTP'
    message = (
        f'Hello {user.username},\n\n'
        f'Your OTP for email verification is: {code}\n\n'
        f'This code will expire in {getattr(settings, "OTP_EXPIRY_MINUTES", 5)} minutes.\n\n'
        f'If you did not request this, please ignore this email.\n\n'
        f'— Vessel Tracker Team'
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return code

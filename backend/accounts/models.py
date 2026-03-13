"""
Accounts models — CustomUser and OTPCode
"""
import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings


class CustomUser(AbstractUser):
    """
    Extended user model with email verification and basic profile details.
    Email is the primary identifier for login.
    """
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    organization = models.CharField(max_length=200, blank=True, default='')
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.email})"


class OTPCode(models.Model):
    """
    One-Time Password for email verification.
    Each OTP expires after OTP_EXPIRY_MINUTES (default 5 min).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='otp_codes'
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"OTP {self.code} for {self.user.email}"

    @property
    def is_expired(self):
        """Check if OTP has expired."""
        expiry_minutes = getattr(settings, 'OTP_EXPIRY_MINUTES', 5)
        return timezone.now() > self.created_at + timezone.timedelta(minutes=expiry_minutes)

    @property
    def is_valid(self):
        """Check if OTP is still usable (not expired and not used)."""
        return not self.is_expired and not self.is_used

    @staticmethod
    def generate_code():
        """Generate a random 6-digit OTP code."""
        return ''.join(random.choices(string.digits, k=6))

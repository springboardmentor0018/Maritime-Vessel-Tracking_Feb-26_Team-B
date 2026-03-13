"""
Accounts serializers — Registration, OTP verification, Login, Profile
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, OTPCode


class RegisterSerializer(serializers.ModelSerializer):
    """Register a new user with email, username, password, and basic details."""
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'confirm_password',
            'phone', 'organization', 'first_name', 'last_name',
        ]

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value.lower()

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            organization=validated_data.get('organization', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_active=True,
            is_email_verified=False,
        )
        return user


class VerifyOTPSerializer(serializers.Serializer):
    """Verify OTP for email confirmation."""
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, min_length=6)

    def validate_email(self, value):
        return value.lower()

    def validate(self, attrs):
        email = attrs['email']
        otp_code = attrs['otp']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'email': 'User not found.'})

        # Find valid OTP
        otp = OTPCode.objects.filter(
            user=user, code=otp_code, is_used=False
        ).order_by('-created_at').first()

        if not otp:
            raise serializers.ValidationError({'otp': 'Invalid OTP code.'})

        if otp.is_expired:
            raise serializers.ValidationError({'otp': 'OTP has expired. Please request a new one.'})

        attrs['user'] = user
        attrs['otp_instance'] = otp
        return attrs


class LoginSerializer(serializers.Serializer):
    """Authenticate with email and password, returns JWT tokens."""
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        return value.lower()

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'email': 'No account found with this email.'})

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError({'password': 'Invalid password.'})

        if not user.is_email_verified:
            raise serializers.ValidationError(
                {'email': 'Email not verified. Please verify your email with OTP first.'}
            )

        attrs['user'] = user
        return attrs


class ResendOTPSerializer(serializers.Serializer):
    """Request a new OTP to be sent to the given email."""
    email = serializers.EmailField()

    def validate_email(self, value):
        value = value.lower()
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('No account found with this email.')
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """Read-only user profile."""
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'organization', 'is_email_verified',
            'created_at', 'updated_at',
        ]
        read_only_fields = fields

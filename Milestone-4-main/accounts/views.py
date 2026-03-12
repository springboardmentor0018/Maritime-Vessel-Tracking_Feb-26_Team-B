"""
Accounts views — Register, OTP verify, Login, Profile, Token refresh
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import (
    RegisterSerializer,
    VerifyOTPSerializer,
    LoginSerializer,
    ResendOTPSerializer,
    UserProfileSerializer,
)
from .models import CustomUser
from .utils import create_and_send_otp


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user and send OTP for email verification.

    POST /api/auth/register/
    Body: { username, email, password, confirm_password, phone?, organization?, first_name?, last_name? }
    """
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    # Send OTP
    try:
        create_and_send_otp(user)
        otp_message = 'OTP sent to your email.'
    except Exception as e:
        otp_message = f'User created but OTP email failed: {str(e)}'

    return Response({
        'success': True,
        'message': f'Registration successful. {otp_message}',
        'data': {
            'username': user.username,
            'email': user.email,
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    """
    Verify email with OTP code.

    POST /api/auth/verify-otp/
    Body: { email, otp }
    """
    serializer = VerifyOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data['user']
    otp_instance = serializer.validated_data['otp_instance']

    # Mark OTP as used
    otp_instance.is_used = True
    otp_instance.save()

    # Verify user email
    user.is_email_verified = True
    user.save()

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)

    return Response({
        'success': True,
        'message': 'Email verified successfully.',
        'data': {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserProfileSerializer(user).data,
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login with email and password, returns JWT tokens.

    POST /api/auth/login/
    Body: { email, password }
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)

    return Response({
        'success': True,
        'message': 'Login successful.',
        'data': {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserProfileSerializer(user).data,
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_otp(request):
    """
    Resend OTP to the given email address.

    POST /api/auth/resend-otp/
    Body: { email }
    """
    serializer = ResendOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    user = CustomUser.objects.get(email=email)

    try:
        create_and_send_otp(user)
        return Response({
            'success': True,
            'message': 'OTP sent to your email.',
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Failed to send OTP: {str(e)}',
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Get the authenticated user's profile.

    GET /api/auth/profile/
    Headers: Authorization: Bearer <access_token>
    """
    serializer = UserProfileSerializer(request.user)
    return Response({
        'success': True,
        'data': serializer.data,
    }, status=status.HTTP_200_OK)

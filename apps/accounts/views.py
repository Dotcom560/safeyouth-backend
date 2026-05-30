# backend/apps/accounts/views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer, UserProfileSerializer

# ============================================
# REGISTER VIEW - Create new user account
# ============================================
class RegisterView(generics.CreateAPIView):
    """
    Register a new user account
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)


# ============================================
# LOGIN VIEW - Authenticate user
# ============================================
class LoginView(APIView):
    """
    Login user and return JWT tokens
    POST /api/auth/login/
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)


# ============================================
# USER PROFILE VIEW - Get current user info
# ============================================
class UserProfileView(APIView):
    """
    Get current user profile
    GET /api/auth/me/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ============================================
# UPDATE PROFILE VIEW - Update user info
# ============================================
class UpdateProfileView(APIView):
    """
    Update user profile
    PATCH /api/auth/profile/
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================
# CHANGE PASSWORD VIEW
# ============================================
class ChangePasswordView(APIView):
    """
    Change user password
    POST /api/auth/change-password/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response({
                'error': 'Both old_password and new_password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(old_password):
            return Response({
                'error': 'Old password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)


# ============================================
# LOGOUT VIEW - Blacklist refresh token
# ============================================
class LogoutView(APIView):
    """
    Logout user by blacklisting refresh token
    POST /api/auth/logout/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({
                'message': 'Logged out successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


# ============================================
# SIMPLE TEST VIEW (for debugging)
# ============================================
class TestAuthView(APIView):
    """
    Simple test endpoint
    GET /api/auth/test/
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            'message': 'Auth API is working!',
            'status': 'ok',
            'available_endpoints': [
                'POST /api/auth/register/',
                'POST /api/auth/login/',
                'GET /api/auth/me/',
                'PATCH /api/auth/profile/',
                'POST /api/auth/change-password/',
                'POST /api/auth/logout/',
            ]
        }, status=status.HTTP_200_OK)
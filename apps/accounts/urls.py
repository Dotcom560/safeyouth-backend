# backend/apps/accounts/urls.py
from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UserProfileView,
    UpdateProfileView,
    ChangePasswordView,
    LogoutView,
    TestAuthView
)

# URL Patterns for Authentication
urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserProfileView.as_view(), name='user_profile'),
    path('profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Test endpoint (for debugging)
    path('test/', TestAuthView.as_view(), name='test_auth'),
]
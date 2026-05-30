# backend/safeyouth_api/urls.py

"""
SafeYouth AI URL Configuration
Main API Gateway for the platform
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# ============================================
# UTILITY VIEWS
# ============================================

def health_check(request):
    """Health check endpoint for monitoring"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'SafeYouth AI API',
        'version': '1.0.0',
        'environment': 'development' if settings.DEBUG else 'production'
    })

def api_root(request):
    """API root with navigation links"""
    endpoints = {
        'message': 'Welcome to SafeYouth AI API',
        'documentation': 'https://docs.safeyouth.ai',
        'endpoints': {
            'health': '/health/',
            'api_root': '/',
            'admin': '/admin/',
        },
        'auth': {
            'token': '/api/token/',
            'refresh': '/api/token/refresh/',
            'verify': '/api/token/verify/',
            'register': '/api/auth/register/',
            'login': '/api/auth/login/',
            'profile': '/api/auth/me/',
        },
        'api_v1': {
            'auth': '/api/auth/',
            'ai_coach': '/api/ai-coach/',
            'help': '/api/help/',
            'learning': '/api/learning/',
            'opportunities': '/api/opportunities/',
            'mood': '/api/mood/',
            'analytics': '/api/analytics/',
            'notifications': '/api/notifications/',
        }
    }
    return JsonResponse(endpoints)

# ============================================
# URL PATTERNS
# ============================================

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),
    
    # Health & Status
    path('health/', health_check, name='health_check'),
    path('', api_root, name='api_root'),
    
    # JWT Authentication - Direct view references
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # ============================================
    # API ENDPOINTS - UNCOMMENTED AND WORKING
    # ============================================
    
    # Authentication & User Management
    path('api/auth/', include('apps.accounts.urls')),
    
    # AI Coach & Voice Assistant
    # path('api/ai-coach/', include('apps.ai_coach.urls')),  # Uncomment when ready
    
    # Help Requests, SOS & Reporting
    # path('api/help/', include('apps.help_requests.urls')),  # Uncomment when ready
    
    # Educational Learning Hub
    # path('api/learning/', include('apps.learning.urls')),  # Uncomment when ready
    
    # Youth Opportunities Feed
    # path('api/opportunities/', include('apps.opportunities.urls')),  # Uncomment when ready
    
    # Mood Tracker & Mental Health
    # path('api/mood/', include('apps.mood_tracker.urls')),  # Uncomment when ready
    
    # Analytics & Reporting Dashboard
    # path('api/analytics/', include('apps.analytics.urls')),  # Uncomment when ready
    
    # Push Notifications
    # path('api/notifications/', include('apps.notifications.urls')),  # Uncomment when ready
]

# ============================================
# DEVELOPMENT URLS
# ============================================

if settings.DEBUG:
    # Static & Media Files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Django Debug Toolbar (if installed)
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass
    
    # API Testing Interface
    def api_test(request):
        return JsonResponse({
            'status': 'API test endpoint working',
            'method': request.method,
            'headers': dict(request.headers),
        })
    
    urlpatterns += [
        path('api-test/', api_test, name='api_test'),
    ]

# ============================================
# ERROR HANDLERS (Production)
# ============================================

if not settings.DEBUG:
    handler400 = 'apps.core.views.bad_request'
    handler403 = 'apps.core.views.permission_denied'
    handler404 = 'apps.core.views.page_not_found'
    handler500 = 'apps.core.views.server_error'
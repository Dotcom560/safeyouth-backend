# backend/safeyouth_api/settings_production.py
"""
SafeYouth AI Production Settings
This file overrides development settings for production environment
"""

from .settings import *
import os
import dj_database_url
import json
import tempfile
from pathlib import Path
import logging

# ============================================
# BASE CONFIGURATION
# ============================================

# Security Settings
DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable is required!")

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')

# Remove empty strings
ALLOWED_HOSTS = [host for host in ALLOWED_HOSTS if host]
CSRF_TRUSTED_ORIGINS = [origin for origin in CSRF_TRUSTED_ORIGINS if origin]

# ============================================
# DATABASE CONFIGURATION (UPDATED)
# ============================================

# Get database URL from environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Parse the database URL
    import urllib.parse
    
    # Handle potential password with special characters
    try:
        # For Render PostgreSQL
        DATABASES = {
            'default': dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True,
                ssl_require=True,  # Required for Render PostgreSQL
                engine='django.db.backends.postgresql',
            )
        }
        print("✅ PostgreSQL database configured from DATABASE_URL")
    except Exception as e:
        print(f"⚠️ Error parsing DATABASE_URL: {e}")
        # Fallback to manual configuration
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('DB_NAME', 'safeyouth_db'),
                'USER': os.environ.get('DB_USER', 'safeyouth_user'),
                'PASSWORD': os.environ.get('DB_PASSWORD', ''),
                'HOST': os.environ.get('DB_HOST', ''),
                'PORT': os.environ.get('DB_PORT', '5432'),
                'OPTIONS': {
                    'sslmode': 'require',
                },
            }
        }
        print("✅ PostgreSQL database configured from individual variables")
else:
    # Fallback to SQLite for development/testing
    import warnings
    warnings.warn("No DATABASE_URL found. Using SQLite. This is not recommended for production!")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("⚠️ Using SQLite database (development mode)")

# Test database connection on startup
try:
    from django.db import connections
    connections['default'].cursor()
    print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")

# ============================================
# STATIC & MEDIA FILES
# ============================================

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Additional static files directories
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []

# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ============================================
# SECURITY HEADERS
# ============================================

# HTTPS and Security Headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Referrer Policy
SECURE_REFERRER_POLICY = 'same-origin'

# ============================================
# CORS CONFIGURATION
# ============================================

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
CORS_ALLOWED_ORIGINS = [origin for origin in CORS_ALLOWED_ORIGINS if origin]

# Fallback to localhost if none specified
if not CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS = [
        'http://localhost:5173',
        'http://localhost:3000',
        'https://*.netlify.app',
    ]
    print("⚠️ Using default CORS origins")

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ============================================
# FIREBASE CONFIGURATION
# ============================================

# Firebase credentials from environment variable or file
firebase_credentials_json = os.environ.get('FIREBASE_CREDENTIALS_JSON')
firebase_credentials_path = os.environ.get('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')

if firebase_credentials_json:
    # Create a temporary file from the JSON string
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(firebase_credentials_json)
            FIREBASE_CREDENTIALS_PATH = f.name
        print("✅ Firebase credentials loaded from environment variable")
    except Exception as e:
        print(f"⚠️ Failed to create Firebase credentials file: {e}")
        FIREBASE_CREDENTIALS_PATH = firebase_credentials_path
else:
    FIREBASE_CREDENTIALS_PATH = firebase_credentials_path
    if os.path.exists(FIREBASE_CREDENTIALS_PATH):
        print(f"✅ Firebase credentials loaded from file: {FIREBASE_CREDENTIALS_PATH}")
    else:
        print(f"⚠️ Firebase credentials not found at: {FIREBASE_CREDENTIALS_PATH}")

FIREBASE_STORAGE_BUCKET = os.environ.get('FIREBASE_STORAGE_BUCKET', 'safeyouth-ai.firebasestorage.app')

# ============================================
# AI CONFIGURATION
# ============================================

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

if not GEMINI_API_KEY:
    print("⚠️ GEMINI_API_KEY not set. AI features will be limited.")

# ============================================
# FIREBASE CLOUD MESSAGING
# ============================================

FCM_SERVER_KEY = os.environ.get('FCM_SERVER_KEY', '')
FCM_SENDER_ID = os.environ.get('FCM_SENDER_ID', '')

# ============================================
# GOOGLE MAPS
# ============================================

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')

# ============================================
# SMS CONFIGURATION (Africa's Talking)
# ============================================

AFRICAS_TALKING_API_KEY = os.environ.get('AFRICAS_TALKING_API_KEY', '')
AFRICAS_TALKING_USERNAME = os.environ.get('AFRICAS_TALKING_USERNAME', '')
SMS_SENDER_ID = os.environ.get('SMS_SENDER_ID', 'SafeYouthAI')

# ============================================
# EMAIL CONFIGURATION
# ============================================

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@safeyouth.com')

# Use console backend if no email credentials are provided
if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    print("⚠️ Email credentials not set. Using console email backend.")
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    print("✅ Email configured with SMTP")

COUNSELOR_EMAIL = os.environ.get('COUNSELOR_EMAIL', 'counselor@safeyouth.com')

# ============================================
# LOGGING CONFIGURATION
# ============================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
        'json': {
            'format': '{"level": "%(levelname)s", "time": "%(asctime)s", "module": "%(module)s", "message": "%(message)s"}',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'INFO',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'production.log'),
            'formatter': 'verbose',
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': os.environ.get('LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

# ============================================
# SENTRY MONITORING (Optional)
# ============================================

SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
if SENTRY_DSN:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration
        
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[
                DjangoIntegration(),
                LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
            ],
            traces_sample_rate=float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', '0.1')),
            send_default_pii=False,
            environment='production',
        )
        print("✅ Sentry monitoring enabled")
    except ImportError:
        print("⚠️ sentry-sdk not installed. Skipping Sentry initialization.")
    except Exception as e:
        print(f"⚠️ Failed to initialize Sentry: {e}")

# ============================================
# CACHE CONFIGURATION
# ============================================

REDIS_URL = os.environ.get('REDIS_URL')
if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'PARSER_CLASS': 'redis.connection.HiredisParser',
                'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
                'CONNECTION_POOL_CLASS_KWARGS': {
                    'max_connections': 50,
                    'timeout': 20,
                },
                'MAX_CONNECTIONS': 1000,
                'PICKLE_VERSION': -1,
            },
            'KEY_PREFIX': 'safeyouth',
            'TIMEOUT': 300,  # 5 minutes
        }
    }
    print("✅ Redis cache configured")
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
    print("⚠️ Using local memory cache (not recommended for production)")

# ============================================
# CELERY CONFIGURATION (Async Tasks)
# ============================================

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', '')
if CELERY_BROKER_URL:
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'django-db')
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60
    CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
    print("✅ Celery configured")

# ============================================
# ADMIN SETTINGS
# ============================================

# Admin interface configuration
ADMIN_SITE_HEADER = "SafeYouth AI Production"
ADMIN_SITE_TITLE = "SafeYouth AI Administration"
ADMIN_INDEX_TITLE = "Welcome to SafeYouth AI Admin Panel"

# ============================================
# STARTUP STATUS
# ============================================

print("=" * 60)
print("🚀 SafeYouth AI Production Settings Loaded")
print("=" * 60)
print(f"🔧 DEBUG Mode: {DEBUG}")
print(f"🌐 Allowed Hosts: {ALLOWED_HOSTS}")
print(f"🗄️ Database: {'PostgreSQL' if DATABASE_URL else 'SQLite'}")
print(f"📁 Static Root: {STATIC_ROOT}")
print(f"📁 Media Root: {MEDIA_ROOT}")
print(f"🔐 CORS Origins: {CORS_ALLOWED_ORIGINS}")
print(f"🤖 Gemini AI: {'Configured' if GEMINI_API_KEY else 'Not configured'}")
print(f"📧 Email: {'SMTP' if EMAIL_HOST_USER else 'Console'}")
print(f"🔥 Firebase: {'Configured' if FIREBASE_CREDENTIALS_PATH else 'Not configured'}")
print("=" * 60)

# Validate critical settings
if not ALLOWED_HOSTS:
    print("⚠️ WARNING: ALLOWED_HOSTS is empty! This may cause issues.")
if not SECRET_KEY:
    print("❌ ERROR: DJANGO_SECRET_KEY is not set!")
if not CORS_ALLOWED_ORIGINS:
    print("⚠️ WARNING: CORS_ALLOWED_ORIGINS is empty!")
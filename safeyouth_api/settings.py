# backend/safeyouth_api/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
import sys

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# Add apps directory to Python path
sys.path.insert(0, str(BASE_DIR / 'apps'))

# ============================================
# SECURITY WARNINGS
# ============================================
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-8x!qq7@2k#9$v&p%m^l*z*c(_f+g=h/j?k,l;:<>?[]{}~`')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ============================================
# SENTRY MONITORING SETUP (Conditional)
# ============================================
SENTRY_DSN = os.getenv('SENTRY_DSN', '')

if SENTRY_DSN and not DEBUG:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        from sentry_sdk.integrations.celery import CeleryIntegration
        from sentry_sdk.integrations.redis import RedisIntegration
        
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[
                DjangoIntegration(),
                CeleryIntegration(),
                RedisIntegration(),
            ],
            traces_sample_rate=float(os.getenv('SENTRY_TRACES_SAMPLE_RATE', '0.1')),
            profiles_sample_rate=float(os.getenv('SENTRY_PROFILES_SAMPLE_RATE', '0.1')),
            send_default_pii=False,
            environment=os.getenv('ENVIRONMENT', 'production'),
            release=os.getenv('GIT_COMMIT_SHA', 'unknown'),
            before_send=lambda event, hint: event,
        )
        print(f"✅ Sentry initialized with DSN: {SENTRY_DSN[:30]}...")
    except ImportError:
        print("⚠️ Sentry SDK not installed. Install with: pip install sentry-sdk[django]")
    except Exception as e:
        print(f"⚠️ Sentry initialization failed: {e}")

# ============================================
# PRODUCTION SECURITY HEADERS
# ============================================
if not DEBUG:
    # Tell Django it's behind a proxy that handles HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Force HTTPS redirect
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True') == 'True'
    
    # Cookie security
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Browser security headers
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ============================================
# APPLICATION DEFINITION
# ============================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'channels',
    'rest_framework_simplejwt',
    'django_filters',
    'whitenoise.runserver_nostatic',
    
    # Celery apps
    'django_celery_results',
    'django_celery_beat',
    
    # Local apps (using 'apps.' prefix since they're in apps folder)
    'apps.core',  # ADDED - Core app for error handlers
    'apps.accounts',
    'apps.ai_coach',
    'apps.help_requests',
    'apps.learning',
    'apps.opportunities',
    'apps.mood_tracker',
    'apps.analytics',
    'apps.notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'safeyouth_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ASGI (for Channels) and WSGI
WSGI_APPLICATION = 'safeyouth_api.wsgi.application'
ASGI_APPLICATION = 'safeyouth_api.asgi.application'

# Channel Layers for real-time features (WebSockets)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',  # Development
        # Production: Use Redis
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #     "hosts": [('127.0.0.1', 6379)],
        # },
    },
}

# ============================================
# DATABASE CONFIGURATION
# ============================================
DATABASE_URL = os.getenv('DATABASE_URL', '')

if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ============================================
# AUTHENTICATION
# ============================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Accra'
USE_I18N = True
USE_TZ = True

# ============================================
# STATIC & MEDIA FILES
# ============================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# CORS SETTINGS
# ============================================
CORS_ALLOW_ALL_ORIGINS = DEBUG

if not DEBUG:
    CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
    CORS_ALLOWED_ORIGINS = [origin for origin in CORS_ALLOWED_ORIGINS if origin]
else:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://safeyouthai.netlify.app",
    ]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_PREFLIGHT_MAX_AGE = 86400

# ============================================
# REST FRAMEWORK SETTINGS
# ============================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny' if DEBUG else 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ) if not DEBUG else (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
}

# ============================================
# JWT SETTINGS
# ============================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
}

# ============================================
# FIREBASE CONFIGURATION
# ============================================
FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')
FIREBASE_STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET', 'safeyouth-ai.firebasestorage.app')
FIREBASE_CREDENTIALS_JSON = os.getenv('FIREBASE_CREDENTIALS_JSON', '')

# ============================================
# AI CONFIGURATION
# ============================================
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# ============================================
# FCM (Firebase Cloud Messaging)
# ============================================
FCM_SERVER_KEY = os.getenv('FCM_SERVER_KEY', '')
FCM_SENDER_ID = os.getenv('FCM_SENDER_ID', '')

# ============================================
# GOOGLE MAPS
# ============================================
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

# ============================================
# SMS CONFIGURATION
# ============================================
AFRICAS_TALKING_API_KEY = os.getenv('AFRICAS_TALKING_API_KEY', '')
AFRICAS_TALKING_USERNAME = os.getenv('AFRICAS_TALKING_USERNAME', '')
SMS_SENDER_ID = os.getenv('SMS_SENDER_ID', 'SafeYouthAI')

# ============================================
# EMAIL CONFIGURATION
# ============================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@safeyouth.com')

COUNSELOR_EMAIL = os.getenv('COUNSELOR_EMAIL', 'counselor@safeyouth.com')

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
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'apps': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Add Sentry handler only if sentry_sdk is available
if SENTRY_DSN and not DEBUG:
    try:
        import sentry_sdk
        LOGGING['handlers']['sentry'] = {
            'level': 'ERROR',
            'class': 'sentry_sdk.integrations.logging.EventHandler',
        }
        LOGGING['loggers']['django.request']['handlers'].append('sentry')
    except ImportError:
        pass

# Ensure logs directory exists
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

# ============================================
# CACHE CONFIGURATION
# ============================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

REDIS_URL = os.getenv('REDIS_URL', '')
if REDIS_URL and not DEBUG:
    try:
        CACHES = {
            'default': {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION': REDIS_URL,
                'OPTIONS': {
                    'client_class': 'django_redis.client.DefaultClient',
                }
            }
        }
        print("✅ Redis cache configured")
    except ImportError:
        print("⚠️ django-redis not installed. Using local memory cache.")

# ============================================
# CELERY CONFIGURATION
# ============================================
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', '')
if CELERY_BROKER_URL:
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'django-db')
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60
    CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60
    CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
    CELERY_CACHE_BACKEND = 'default'
    CELERY_RESULT_EXTENDED = True
    print("✅ Celery configured")
else:
    print("⚠️ CELERY_BROKER_URL not set. Celery tasks will run synchronously.")

# ============================================
# DJANGO ADMIN SETTINGS
# ============================================
ADMIN_SITE_HEADER = "SafeYouth AI Administration"
ADMIN_SITE_TITLE = "SafeYouth AI Admin"
ADMIN_INDEX_TITLE = "Welcome to SafeYouth AI Admin Panel"

# ============================================
# STARTUP STATUS
# ============================================
print("=" * 60)
print(f"✅ Settings loaded with DEBUG={DEBUG}")
print(f"📁 Base directory: {BASE_DIR}")
print(f"🔧 Apps directory: {BASE_DIR / 'apps'}")
print(f"🗄️ Database: {'PostgreSQL' if DATABASE_URL else 'SQLite'}")
print(f"🔐 CORS Mode: {'Allow All' if CORS_ALLOW_ALL_ORIGINS else 'Restricted'}")
if not CORS_ALLOW_ALL_ORIGINS:
    print(f"   Allowed Origins: {CORS_ALLOWED_ORIGINS}")
print("=" * 60)

if SENTRY_DSN and not DEBUG:
    print(f"✅ Sentry monitoring enabled")
else:
    print(f"⚠️ Sentry monitoring disabled (DSN not set or DEBUG=True)")
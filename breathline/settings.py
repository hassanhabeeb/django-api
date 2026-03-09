import os, dj_database_url, datetime, ast, warnings
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from django.core.management.utils import get_random_secret_key
from django.core.validators import URLValidator
from typing import List, Optional

# Load .env file
load_dotenv(find_dotenv(), override=True, verbose=True)

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Helper Functions ---
def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return default_value
    return default_value

def get_list(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [v.strip() for v in value.split(',') if v.strip()]

# --- Security Settings ---
# FIX: Fallback key allows Docker build to succeed without ENV vars
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-build-placeholder-key-123')

DEBUG = get_bool_from_env("DEBUG", False)

# In production, this is handled by the Load Balancer DNS
ALLOWED_HOSTS = get_list(os.environ.get("ALLOWED_HOSTS", "*"))

# --- Application definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third Party
    'drf_yasg',
    'debug_toolbar',
    'django_extensions',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_acl',
    'encrypted_model_fields',
    # Local Apps
    'apps.user',
    'apps.authentication',
    'apps.home',
    'apps.blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # FIX: Crucial for serving CSS/JS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'breathline.urls'

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

WSGI_APPLICATION = 'breathline.wsgi.application'

# --- Database ---
# FIX: Default to 5432 and dummy strings so Docker build doesn't fail
try:
    database_port = int(os.environ.get('DATABASE_PORT', 5432))
except (ValueError, TypeError):
    database_port = 5432

DATABASES = {
    'default': dj_database_url.config(
        default=f"postgres://{os.environ.get('DATABASE_USER', 'user')}:{os.environ.get('DATABASE_PASSWORD', 'pass')}@{os.environ.get('DATABASE_HOST', 'localhost')}:{database_port}/{os.environ.get('DATABASE_NAME', 'db')}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

DATABASE_ROUTERS = ['breathline.database_router.UserBasedRouter']

# --- Static & Media Files ---
# FIX: WhiteNoise configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Enable WhiteNoise compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- Auth & Internationalization ---
AUTH_USER_MODEL = "user.Users"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
APPEND_SLASH = False
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- CORS & DRF Settings ---
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'breathline.exceptions.exceptions.handle_exception',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTTokenUserAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=20),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=50),
    'SIGNING_KEY': os.environ.get('SECRET_KEY', SECRET_KEY), # Uses placeholder if ENV missing
    'AUTH_HEADER_TYPES': ('Bearer',),
}

SWAGGER_SETTINGS = {
    'DEFAULT_API_URL': os.environ.get('SWAGGER_DEFAULT_API_URL', ""),
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'}
    },
}

# --- Logging ---
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

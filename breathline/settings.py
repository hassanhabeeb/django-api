import os, dj_database_url, datetime, ast
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Load .env file
load_dotenv(find_dotenv(), override=True)

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

# --- Core Security ---
# Placeholder for Docker build phase so collectstatic works
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-build-placeholder-key-123')
DEBUG = get_bool_from_env("DEBUG", False)
ALLOWED_HOSTS = ["*"]  # Since ALB DNS names can change

# --- Application Definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third Party
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    # Local Apps
    'apps.user',
    'apps.authentication',
    'apps.home',
    'apps.blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # CRITICAL: WhiteNoise must be exactly here to serve files on HTTP
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'breathline.urls'

WSGI_APPLICATION = 'breathline.wsgi.application'

# --- Database (AWS RDS / Secrets Manager) ---
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'postgres://user:pass@localhost:5432/db'),
        conn_max_age=600,
    )
}

# --- Static Files (The 404 & MIME Fix) ---
# Leading slash is mandatory for the browser to find files relative to the root
STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Simplified storage to avoid manifest/hashing issues during testing
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# --- HTTP-Only Security Settings (Fixes "Untrustworthy Origin") ---
# We disable these because we do not have an SSL certificate/Domain
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SECURE_REFERRER_POLICY = None
# Tells Django to trust the ALB header even if it's just HTTP for now
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- CORS Settings ---
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# --- Swagger / DRF ---
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'VALIDATOR_URL': None, # Prevents Swagger from trying to call an external validator
    'SECURITY_DEFINITIONS': {
        'Bearer': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'}
    },
}

# --- Templates ---
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

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

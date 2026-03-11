import os
import dj_database_url
import ast
import mimetypes
import json
import boto3
from pathlib import Path
from botocore.exceptions import ClientError

# ---------------------------------------------------------------------------
# Base Directory
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# AWS Secrets Manager Helper
# ---------------------------------------------------------------------------
def get_secrets_from_aws():
    """
    Fetches database credentials from AWS Secrets Manager for ap-south-1.
    """
    secret_name = "breathline/db-credentials"
    region_name = "ap-south-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            return json.loads(get_secret_value_response['SecretString'])
    except ClientError as e:
        # Fallback to console print for debugging during container startup
        print(f"⚠️ AWS Secrets Manager fetch failed: {e}")
        return None
    return None

# ---------------------------------------------------------------------------
# MIME helpers
# ---------------------------------------------------------------------------
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("application/javascript", ".js", True)

# ---------------------------------------------------------------------------
# Core Security & Debug
# ---------------------------------------------------------------------------
SECRET_KEY = os.environ.get('SECRET_KEY', 'build-key-123')
DEBUG = ast.literal_eval(os.environ.get('DEBUG', 'False'))
ALLOWED_HOSTS = ["*"]

# ---------------------------------------------------------------------------
# Apps
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'django_acl',
    'apps.user',
    'apps.authentication',
    'apps.home',
    'apps.blog',
]

# ---------------------------------------------------------------------------
# Middleware (WhiteNoise MUST be immediately after SecurityMiddleware)
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------------------------------------------------------
# Templates (Fixes admin.E403 Error)
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Static files (WhiteNoise & StaticRoot)
# ---------------------------------------------------------------------------
STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.environ.get('STATIC_ROOT') or os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Storage logic for drf-yasg compatibility
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_ALLOW_ALL_ORIGINS = True
WHITENOISE_AUTOREFRESH = False

# ---------------------------------------------------------------------------
# Security / Proxy Settings
# ---------------------------------------------------------------------------
SECURE_SSL_REDIRECT = False
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# ---------------------------------------------------------------------------
# URLs / WSGI / Auth
# ---------------------------------------------------------------------------
ROOT_URLCONF = 'breathline.urls'
WSGI_APPLICATION = 'breathline.wsgi.application'
AUTH_USER_MODEL = 'user.Users'

# ---------------------------------------------------------------------------
# Database (AWS RDS + Secrets Manager)
# ---------------------------------------------------------------------------
aws_db_secrets = get_secrets_from_aws()

if aws_db_secrets:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql', # Change to .mysql if RDS is MySQL
            'NAME': aws_db_secrets.get('dbname') or aws_db_secrets.get('dbInstanceIdentifier'),
            'USER': aws_db_secrets.get('username'),
            'PASSWORD': aws_db_secrets.get('password'),
            'HOST': aws_db_secrets.get('host'),
            'PORT': aws_db_secrets.get('port', '5432'),
            'CONN_MAX_AGE': 600,
        }
    }
else:
    # Fallback for local development or if AWS Secrets fetch fails
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
            conn_max_age=600,
        )
    }

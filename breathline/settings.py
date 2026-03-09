import os, dj_database_url, ast
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECRETS & BUILD COMPATIBILITY ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-build-placeholder')
DEBUG = ast.literal_eval(os.environ.get('DEBUG', 'False'))
ALLOWED_HOSTS = ["*"] 

# --- APPLICATION DEFINITION ---
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
    'django_acl',  # <--- Ensure this is the correct package name
    # Local Apps
    'apps.user',
    'apps.authentication',
    'apps.home',
    'apps.blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Position is vital
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

# --- DATABASE ---
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'postgres://u:p@localhost:5432/db'),
        conn_max_age=600,
    )
}

# --- STATIC FILES (Stop 404s/MIME errors) ---
STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# --- HTTP-ONLY SECURITY (Fix "Untrustworthy Origin") ---
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# --- SWAGGER ---
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'VALIDATOR_URL': None,
}

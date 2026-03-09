import os, dj_database_url, ast
from pathlib import Path

# settings.py additions

# Force WhiteNoise to ignore "untrusted" origins for its own internal checks
WHITENOISE_ALLOW_ALL_ORIGINS = True

# This helps WhiteNoise determine the correct MIME types
import mimetypes
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("application/javascript", ".js", True)


BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'build-key-123')
DEBUG = ast.literal_eval(os.environ.get('DEBUG', 'False'))
ALLOWED_HOSTS = ["*"]

# --- Apps ---
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
    'django_acl', # MUST BE HERE
    'apps.user',
    'apps.authentication',
    'apps.home',
    'apps.blog',
]

# --- WhiteNoise & Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Fixed 404/MIME
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- Static Files ---
STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# CompressedManifestStaticFilesStorage writes a staticfiles.json manifest with
# content-hashed filenames. WhiteNoise uses this to reliably serve all assets
# (including drf-yasg / swagger) without 404s or MIME-type mismatches.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_INDEX_FILE = True

# --- Security / Proxy / HTTPS ---
# Set only if your ALB is terminating HTTPS and forwarding X-Forwarded-Proto.
# If your ALB listener is HTTP-only (port 80), comment this line out.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False           # Don't force HTTPS at the app level
SECURE_CROSS_ORIGIN_OPENER_POLICY = None  # Suppress COOP header (HTTP ALB)
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

ROOT_URLCONF = 'breathline.urls'
WSGI_APPLICATION = 'breathline.wsgi.application'
AUTH_USER_MODEL = 'user.Users'

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600,
    )
}

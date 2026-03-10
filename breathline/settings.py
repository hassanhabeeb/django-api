import os, dj_database_url, ast, mimetypes
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# MIME helpers – ensures WhiteNoise/Django serve correct Content-Type headers
# ---------------------------------------------------------------------------
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("application/javascript", ".js", True)

# ---------------------------------------------------------------------------
# Core
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
# Middleware  (WhiteNoise MUST be immediately after SecurityMiddleware)
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
# Static files
# ---------------------------------------------------------------------------
STATIC_URL = '/staticfiles/'
# Read from env so Dockerfile ENV STATIC_ROOT=/srv/staticfiles is honoured.
# Default keeps local dev working without setting any env var.
STATIC_ROOT = os.environ.get('STATIC_ROOT') or os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# CompressedStaticFilesStorage: serves files at their ORIGINAL paths (no hash
# suffix).  This is required because drf-yasg renders its Swagger HTML with
# hard-coded non-hashed paths like /staticfiles/drf-yasg/style.css.
# CompressedManifestStaticFilesStorage renames files with hashes, so those
# hard-coded paths return 404 – DO NOT use it with drf-yasg.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# WhiteNoise settings
WHITENOISE_ALLOW_ALL_ORIGINS = True   # Serve to any origin (ALB, CDN, etc.)
WHITENOISE_AUTOREFRESH = False        # Keep False in prod for performance

# ---------------------------------------------------------------------------
# Security / ALB proxy headers
# ---------------------------------------------------------------------------
# Because your ALB listener is HTTP (not HTTPS), we must NOT set
# SECURE_PROXY_SSL_HEADER – doing so makes Django think every request is
# HTTPS, which triggers the "COOP header ignored" browser warning.
# Uncomment the line below ONLY AFTER you add an HTTPS listener to your ALB.
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = False
SECURE_CROSS_ORIGIN_OPENER_POLICY = None   # Suppress COOP header on HTTP
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# ---------------------------------------------------------------------------
# URLs / WSGI
# ---------------------------------------------------------------------------
ROOT_URLCONF = 'breathline.urls'
WSGI_APPLICATION = 'breathline.wsgi.application'
AUTH_USER_MODEL = 'user.Users'

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600,
    )
}
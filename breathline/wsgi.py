# breathline/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'breathline.settings')

application = get_wsgi_application()

# NOTE: Static files are served by WhiteNoiseMiddleware (configured in
# settings.py MIDDLEWARE list).  It reads STATIC_ROOT and STATIC_URL
# automatically — no manual WSGI wrapping is needed.

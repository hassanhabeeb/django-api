# breathline/wsgi.py
import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise # <--- Add this

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'breathline.settings')

application = get_wsgi_application()

# Explicitly wrap the application with WhiteNoise
# This forces the container to look in /app/staticfiles for any /staticfiles/ URL
application = WhiteNoise(application, root='/app/staticfiles')
application.add_files('/app/staticfiles', prefix='staticfiles/')

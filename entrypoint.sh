#!/bin/bash
set -e

echo "=========================================="
echo " Container startup: collecting static files"
echo "=========================================="

# Run collectstatic at container start time so static files are ALWAYS
# present — even if an ECS volume mount shadows what was baked into the image.
# --skip-checks avoids running DB health checks (DB may not be needed here)
python manage.py collectstatic --noinput --clear --skip-checks

# Sanity check: fail loudly if key drf-yasg assets are still missing
if [ ! -f "${STATIC_ROOT:-/srv/staticfiles}/drf-yasg/style.css" ]; then
    echo "ERROR: drf-yasg static files missing after collectstatic — aborting."
    exit 1
fi

echo "✅ Static files ready at ${STATIC_ROOT:-/srv/staticfiles}"
echo "=========================================="
echo " Starting Gunicorn"
echo "=========================================="

exec gunicorn breathline.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -

#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting Entrypoint Script..."

echo "📦 Creating migrations..."
python manage.py makemigrations --noinput

echo "📦 Applying database migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting Gunicorn..."

exec gunicorn breathline.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120

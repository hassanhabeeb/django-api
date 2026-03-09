FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dummy SECRET_KEY only for the build step (collectstatic).
# The real SECRET_KEY is injected at runtime via ECS task environment variables.
ENV SECRET_KEY=build-time-dummy-secret-key-not-used-in-prod
ENV DEBUG=False
ENV DATABASE_URL=sqlite:////tmp/build.db

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Collect static files (drf-yasg, admin, etc.)
# --noinput : non-interactive
# --clear   : wipe old stale files first
# No --skip-checks so Django validates apps + finders properly
RUN python manage.py collectstatic --noinput --clear

# Verify drf-yasg static files were collected
RUN ls /app/staticfiles/drf-yasg/ && echo "✅ drf-yasg statics collected OK"

EXPOSE 8000

CMD ["gunicorn", "breathline.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

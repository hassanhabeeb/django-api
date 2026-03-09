FROM python:3.11-slim

# ── Environment ──────────────────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dummy values for build-time only (real secrets are injected by ECS at runtime)
ENV SECRET_KEY=build-time-dummy-key
ENV DEBUG=False
# Use sqlite so collectstatic doesn't need a real DB connection
ENV DATABASE_URL=sqlite:////tmp/scratch.db

WORKDIR /app

# ── System deps ──────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# ── Python deps ──────────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── App code ─────────────────────────────────────────────────────────────────
COPY . .

# ── Collect static files ─────────────────────────────────────────────────────
# --noinput   : non-interactive
# --clear     : remove stale files from a previous build layer
# No --skip-checks → Django validates all INSTALLED_APPS static finders,
# ensuring drf-yasg, admin, and every other app is included.
RUN python manage.py collectstatic --noinput --clear

# Fail the build explicitly if the key drf-yasg assets are missing
RUN test -f /app/staticfiles/drf-yasg/style.css \
    && test -f /app/staticfiles/drf-yasg/swagger-ui-dist/swagger-ui.css \
    && test -f /app/staticfiles/drf-yasg/swagger-ui-dist/swagger-ui-bundle.js \
    && echo "✅  drf-yasg static files verified OK" \
    || (echo "❌  drf-yasg static files MISSING – build failed" && exit 1)

# ── Runtime ──────────────────────────────────────────────────────────────────
EXPOSE 8000
CMD ["gunicorn", "breathline.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]

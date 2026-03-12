FROM python:3.11-slim

# ── Environment ──────────────────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV STATIC_ROOT=/srv/staticfiles

# Dummy build-time values to satisfy Django initialization
ENV SECRET_KEY=build-time-dummy-key
ENV DEBUG=False
# Redirecting to local sqlite for build-time only
ENV DATABASE_URL=sqlite:////tmp/scratch.db 

WORKDIR /app

# ── System deps ──────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ── Python setup ─────────────────────────────────────────────────────────────
RUN python -m venv $VIRTUAL_ENV

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir boto3

# ── App code ─────────────────────────────────────────────────────────────────
COPY . .

# ── Collect static files ─────────────────────────────────────────────────────
# We explicitly set the settings module to ensure it picks up our IS_COLLECTSTATIC check
RUN mkdir -p /srv/staticfiles && \
    DJANGO_SETTINGS_MODULE=breathline.settings \
    python manage.py collectstatic --noinput --clear --skip-checks && \
    echo "✅ Build-time static collection done"

# ── Entrypoint ───────────────────────────────────────────────────────────────
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
CMD ["/entrypoint.sh"]

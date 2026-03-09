FROM python:3.11-slim

# ── Environment ──────────────────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Static files are stored at /srv/staticfiles — OUTSIDE /app — so any ECS
# volume mount on /app cannot shadow them.
ENV STATIC_ROOT=/srv/staticfiles

# Dummy build-time values (real secrets injected by ECS at runtime)
ENV SECRET_KEY=build-time-dummy-key
ENV DEBUG=False
ENV DATABASE_URL=sqlite:////tmp/scratch.db

WORKDIR /app

# ── System deps ──────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# ── Python deps ──────────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── App code ─────────────────────────────────────────────────────────────────
COPY . .

# ── Collect static files at BUILD time (layer cache benefit) ─────────────────
RUN mkdir -p /srv/staticfiles && \
    python manage.py collectstatic --noinput --clear --skip-checks && \
    echo "✅ Build-time static collection done" && \
    ls /srv/staticfiles/drf-yasg/swagger-ui-dist/swagger-ui-bundle.js

# ── Entrypoint (also runs collectstatic at container START time) ──────────────
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
CMD ["/entrypoint.sh"]

FROM python:3.11-slim

# ── Environment ──────────────────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set the path to the virtual environment
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV STATIC_ROOT=/srv/staticfiles

# Dummy build-time values
ENV SECRET_KEY=build-time-dummy-key
ENV DEBUG=False
# Using a local sqlite for build-time collectstatic to avoid RDS connection
ENV DATABASE_URL=sqlite:////tmp/scratch.db 

WORKDIR /app

# ── System deps ──────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ── Python venv & deps ───────────────────────────────────────────────────────
# Create the virtual environment
RUN python -m venv $VIRTUAL_ENV

COPY requirements.txt .
# Ensure boto3 is present for Secrets Manager logic in settings.py
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir boto3

# ── App code ─────────────────────────────────────────────────────────────────
COPY . .

# ── Collect static files at BUILD time ───────────────────────────────────────
# We run this inside the venv (inherited from PATH)
RUN mkdir -p /srv/staticfiles && \
    python manage.py collectstatic --noinput --clear --skip-checks && \
    echo "✅ Build-time static collection done"

# ── Entrypoint ───────────────────────────────────────────────────────────────
# Copy entrypoint from project root to container root
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
CMD ["/entrypoint.sh"]

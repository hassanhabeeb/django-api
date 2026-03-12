FROM public.ecr.aws/docker/library/python:3.11-slim

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

# After your requirements are installed...

# Copy custom auth migration to the container's django library
# We use a python script to reliably find the site-packages path to avoid bash/venv escaping issues
COPY custom_migrations/auth/0013_role_permission_label_permission_sub_label.py /tmp/patch_0013.py
COPY custom_migrations/django_acl/0001_initial.py /tmp/patch_acl.py

RUN python -c "\
import os, shutil, django.contrib.auth.migrations as auth_m, django_acl.migrations as acl_m; \
auth_dir = os.path.dirname(auth_m.__file__); \
acl_dir = os.path.dirname(acl_m.__file__); \
shutil.copy('/tmp/patch_0013.py', os.path.join(auth_dir, '0013_role_permission_label_permission_sub_label.py')); \
shutil.copy('/tmp/patch_acl.py', os.path.join(acl_dir, '0001_initial.py')); \
print('✅ Auth and ACL migrations injected dynamically.')"

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

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# --- ADD THIS PART ---
# Gather all static files (CSS, JS, Images) into the staticfiles folder
RUN python manage.py collectstatic --noinput
# ---------------------

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["gunicorn", "breathline.wsgi:application", "--bind", "0.0.0.0:8000"]

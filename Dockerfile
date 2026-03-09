FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (if needed for psycopg2 etc)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Now that whitenoise and your code are inside, collect static files
# We use the dummy SECRET_KEY here just in case, though it's in settings.py now
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "breathline.wsgi:application", "--bind", "0.0.0.0:8000"]

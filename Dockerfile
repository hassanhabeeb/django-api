FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# FIX: Run collectstatic to generate the folder WhiteNoise needs
RUN python manage.py collectstatic --noinput
RUN ls -R /app/staticfiles/drf-yasg/

EXPOSE 8000

# FIX: Corrected the typo "bredocker" to "breathline"
CMD ["gunicorn", "breathline.wsgi:application", "--bind", "0.0.0.0:8000"]

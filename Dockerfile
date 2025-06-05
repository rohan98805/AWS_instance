# Use a slim Python base image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Clean .pyc and __pycache__ files
RUN find . -type f -name "*.pyc" -delete && \
    find . -type d -name "__pycache__" -exec rm -rf {} +

# Collect static files and run migrations (optional if already handled in Jenkins)
RUN python manage.py collectstatic --noinput || true
RUN python manage.py migrate || true

# Expose the Django port
EXPOSE 8000

# Run the Django app using Gunicorn
CMD ["gunicorn", "LandManagementSystem.wsgi:application", "--bind", "0.0.0.0:8000"]

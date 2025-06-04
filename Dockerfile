# Use a slim Python base image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies required for psycopg2 and others
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Collect static files and run migrations (optional at build time)
RUN python manage.py collectstatic --noinput

# Consider running `migrate` at container startup, not build time
# RUN python manage.py migrate

# Expose the default port
EXPOSE 8000

# Start the application with Gunicorn
CMD ["gunicorn", "LandManagementSystem.wsgi:application", "--bind", "0.0.0.0:8000"]

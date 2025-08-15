# Multi-stage build for Django + React + GraphQL app
FROM node:18-alpine AS frontend-builder

# Set working directory for frontend build
WORKDIR /app

# Copy package files and webpack config
COPY package*.json ./
COPY webpack.config.js ./

# Copy frontend source code
COPY frontend/ ./frontend/

# Install Node.js dependencies (including dev dependencies for build)
RUN npm ci

# Build frontend for production (npm ci runs postinstall automatically)

# Python runtime stage
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=statsdontlie.settings

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Copy built frontend assets from previous stage
COPY --from=frontend-builder /app/assets/ ./assets/

# Create static files directory
RUN mkdir -p /app/static

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "statsdontlie.wsgi:application"]
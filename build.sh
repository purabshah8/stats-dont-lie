#!/usr/bin/env bash
# Build script for stats-dont-lie (Railway deployment)

set -o errexit  # Exit on error

# Build frontend assets (npm ci already run by Nixpacks)
echo "Building production frontend assets..."
npm run postinstall

# Collect static files for Django
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Seed data if SEED_DATA environment variable is set to true
if [ "$SEED_DATA" = "true" ]; then
    echo "Seeding database with initial data..."
    python create_db.py
else
    echo "Skipping data seeding (SEED_DATA not set to true)"
fi

echo "Build completed successfully!"
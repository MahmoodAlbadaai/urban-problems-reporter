#!/bin/sh
set -ex
sleep 10

# Move to the /app folder
cd /app

# Run any new database migrations
python manage.py migrate

# Create admin superuser if it doesn't already exist
python manage.py createsuperuser --noinput || true

# Start the Django development server
python manage.py runserver 0.0.0.0:8000

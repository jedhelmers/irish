#!/bin/bash

set -e

# wait-for-postgres.sh
while ! nc -z db 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# Run migrations
python manage.py migrate

# Populate the database (new line added)
python populate_tags.py

# Run your server
exec "$@"

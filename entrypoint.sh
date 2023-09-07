#!/bin/bash

# Wait for the database to be available
until python manage.py dbshell; do
    echo "Waiting for the PostgreSQL service to start..."
    sleep 1
done

# Run migrations
python manage.py migrate

# Populate the database (new line added)
python populate_tags.py

# Run your server
exec "$@"

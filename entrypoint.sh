#!/bin/bash

set -e

# Run migrations
python manage.py migrate

# Populate the database
# python populate_tags.py

# Run your server
exec "$@"

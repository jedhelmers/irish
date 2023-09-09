#!/bin/bash

set -e

/scripts/wait-for-it.sh db:5432 --timeout=30

# wait-for-postgres.sh
until PGPASSWORD=mypassword psql -h "db" -U "myuser" -d "mydatabase" -c '\l'; do
  echo "Postgres is unavailable - sleeping..."
  sleep 1
done


# Run migrations
python manage.py migrate

# Populate the database (new line added)
python populate_tags.py

# Run your server
exec "$@"

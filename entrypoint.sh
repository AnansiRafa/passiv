#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z db 5432; do
  echo "Still waiting for DB..."
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py migrate
exec "$@"

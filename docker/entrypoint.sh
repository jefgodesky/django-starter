#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for PostgreSQL..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

if [ "$DEBUG" = "1" ]; then
  python manage.py flush --no-input
  python manage.py migrate
  exec "$@"
else
  exec gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 1 --timeout 0 "$SITENAME.wsgi:application"
fi

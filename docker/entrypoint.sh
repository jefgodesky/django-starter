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
  poetry run python manage.py flush --no-input
  poetry run python manage.py migrate
fi

exec "$@"

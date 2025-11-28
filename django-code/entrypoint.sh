#!/bin/sh

echo "Running database migrations..."
python manage.py migrate --verbosity 3

echo "Starting uvicorn server..."
exec uvicorn mysite.asgi:application --host 0.0.0.0 --port 8000
#!/bin/sh

# local output static files in settings.py
SOURCE_PATH="/app/staticfiles"
# target path to be shared with nginx
DEST_PATH="/vol/web/static"

echo "Collecting static files to local path ($SOURCE_PATH)..."
python manage.py collectstatic --noinput

echo "Copying static files from $SOURCE_PATH to mounted volume $DEST_PATH..."
cp -rv "$SOURCE_PATH"/* "$DEST_PATH"

echo "Running database migrations..."
python manage.py migrate --verbosity 3

echo "Starting uvicorn server..."
exec uvicorn mysite.asgi:application --host 0.0.0.0 --port 8000
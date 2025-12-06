#!/bin/sh

#### RUN collect static files into shared volume ####
# local output static files in settings.py
SOURCE_PATH="/app/staticfiles"
# target path to be shared with nginx
DEST_PATH="/vol/web/static"

echo "Collecting static files to local path ($SOURCE_PATH)..."
python manage.py collectstatic --noinput

echo "Copying static files from $SOURCE_PATH to mounted volume $DEST_PATH..."
cp -rv "$SOURCE_PATH"/* "$DEST_PATH"

#### RUN migrations ####
echo "Running database migrations..."
python manage.py migrate --verbosity 3

#### RUN create superuser ####
ENV_FILE="/app/.admin.env"

# 1. Check if the file exists
if [ -f "$ENV_FILE" ]; then
    echo "Loading environment variables from $ENV_FILE"
    set -o allexport 
    . "$ENV_FILE"
    set +o allexport
else
    echo "Warning: .env file not found at $ENV_FILE"
fi

ADMIN_USER=$(echo "$USER" | tr -d '[:space:]')
ADMIN_PASSWORD=$(echo "$PASSWORD" | tr -d '[:space:]')
ADMIN_EMAIL=$(echo "$EMAIL" | tr -d '[:space:]')

echo "user is: $ADMIN_USER"
echo "pwd is: $ADMIN_PASSWORD"

export DJANGO_SUPERUSER_PASSWORD="$ADMIN_PASSWORD"
python manage.py createsuperuser \
    --noinput \
    --username "$ADMIN_USER" \
    --email "$ADMIN_EMAIL"

#### RUN start server ####
echo "Starting uvicorn server..."
exec uvicorn mysite.asgi:application --host 0.0.0.0 --port 8000
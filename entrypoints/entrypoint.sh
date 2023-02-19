#!/bin/sh

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

echo "DB started"

while ! nc -z $REDIS_HOST $REDIS_PORT; do
  sleep 0.1
done

echo "Redis started"

echo "Doing migrations..."
python manage.py migrate --settings=f1.settings.production
echo "Migrations Done."

echo "Loading data..."
python manage.py load_data --settings=f1.settings.production
echo "Data Loading Done."

echo "Starting server"
gunicorn -w 3 --max-requests 200 --log-level info --worker-tmp-dir /dev/shm --bind 0.0.0.0:8000 f1.wsgi

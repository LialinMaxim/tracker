release: python ./service/scripts/create_superuser.py; python manage.py migrate;
web: daphne helitrack.asgi:application --port $PORT --bind 0.0.0.0 -v2


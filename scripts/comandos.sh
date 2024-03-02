#!/bin/sh

# o shell irá encerrar a execução do script quando um comando falhar
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "Aguardando o Postgres iniciar ($POSTGRES_HOST $POSTGRES_PORT)..."
    sleep 5
done

echo "Postgres iniciado com sucesso ($POSTGRES_HOST $POSTGRES_PORT)"

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput
gunicorn pytudo.wsgi:application --bind 0.0.0.0:8000

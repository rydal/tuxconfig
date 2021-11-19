# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL="postgresql://tuxconfig:CDYrikFcKtrkwlRl@default-postgresql-do-user-6623180-0.b.db.ondigitalocean.com:25060/tuxconfig?sslmode=require"
ENV DJANGO_SETTINGS_MODULE=tuxconfig_django.settings 
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "tuxconfig_django.wsgi"]
EXPOSE 8000

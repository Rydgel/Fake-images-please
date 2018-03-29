FROM tiangolo/uwsgi-nginx-flask:python3.6

MAINTAINER Jérôme Mahuet <jerome.mahuet@gmail.com>

ENV NGINX_WORKER_PROCESSES auto
ENV STATIC_PATH /app/static

RUN pip install --upgrade pip
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

COPY ./app /app

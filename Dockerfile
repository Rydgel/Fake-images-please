FROM tiangolo/meinheld-gunicorn-flask:python3.7-alpine3.8

LABEL maintainer="Jérôme Mahuet <jerome.mahuet@gmail.com>"

RUN apk --update --no-cache add \
    build-base \
    python-dev \
    jpeg-dev \
    libpng \
    zlib-dev \
    freetype-dev

ENV LIBRARY_PATH=/lib:/usr/lib

ENV NGINX_WORKER_PROCESSES auto
ENV STATIC_PATH /app/static

RUN pip install --upgrade pip
ADD requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

EXPOSE 80

COPY ./app /app

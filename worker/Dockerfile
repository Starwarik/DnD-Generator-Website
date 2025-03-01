FROM python:3.11.2-alpine3.17

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/*

COPY ./worker /code/worker

CMD ["celery", "-A", "worker.main:celery_app", "worker", "--loglevel=INFO"]

FROM python:3.11.2-alpine3.17

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --root-user-action=ignore --upgrade --no-cache-dir && \
 apk --purge del .build-deps

COPY ./worker /code/worker
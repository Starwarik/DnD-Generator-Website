FROM python:3.11.2-slim-buster

WORKDIR /code

RUN pip install --upgrade pip

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --root-user-action=ignore --upgrade -r requirements.txt

COPY ./worker /code/worker

WORKDIR /code/worker
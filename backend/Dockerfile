FROM python:3.11.2-slim-buster

WORKDIR /code

RUN pip install --upgrade pip

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN mkdir -p /code/data && chmod -R 777 /code/data 

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
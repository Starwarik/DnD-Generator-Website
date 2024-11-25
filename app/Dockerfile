FROM python:3.11.2-slim-buster

WORKDIR /code

RUN pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app ./code/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
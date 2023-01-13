FROM python:3.10.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app/
WORKDIR /app/

RUN apt update && apt install libpq-dev gcc -y

COPY ./django/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn psycopg2

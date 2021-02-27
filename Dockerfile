FROM python:3.9

WORKDIR /usr/src/ecommerce_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install netcat -y
RUN apt-get update && apt-get install postgresql gcc python3-dev musl-dev -y

RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip install -r req.txt

COPY . /usr/src/ecommerce_app

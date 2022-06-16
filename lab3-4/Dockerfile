# syntax=docker/dockerfile:1
FROM python:3.8.5-alpine
FROM ubuntu:20.04
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code

RUN apt-get update
RUN apt-get install -y gcc python3-dev python3-pip libffi-dev libpq-dev

COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/
ADD . /code/

EXPOSE 8000
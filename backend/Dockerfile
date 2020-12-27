FROM python:3.8-slim-buster

ARG DJANGO_ENV

RUN apt-get update \
	&& apt-get install -yq \
	libpq-dev \
	build-essential \
	netcat \
	&& pip install poetry

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install

COPY . /app

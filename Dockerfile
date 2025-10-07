FROM python:3.13-slim

RUN mkdir /opt/app

WORKDIR /opt/app

RUN apt update && apt install -y \
    make \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install poetry

COPY . /opt/app
RUN poetry install --no-interaction --no-ansi

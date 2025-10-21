FROM python:3.13-slim

# ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG UID=1000
ARG GID=1000

RUN apt update && apt install -y \
    vim \
    make \
    gcc \
    gettext \
    graphviz \
    graphviz-dev \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install poetry

RUN groupadd -g "${GID}" django && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" django

RUN mkdir /opt/app
RUN chown "${UID}:${GID}" /opt/app

USER django

WORKDIR /opt/app

COPY --chown="${UID}:${GID}" . /opt/app

RUN poetry install --no-interaction --no-ansi

WORKDIR /opt/app/project

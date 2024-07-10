FROM python:3.12-slim

ARG UID=1000
ARG GID=1000

RUN apt update && apt install -y \
    make \
    less \
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

COPY --chown="${UID}:${GID}" pyproject.toml poetry.* /opt/app
RUN poetry install --no-interaction --no-ansi

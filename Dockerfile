# NuPyServer Docker
FROM python:3.7-slim-buster
RUN apt update \
    && apt install build-essential libssl-dev python3-dev libffi-dev cargo -y \
    && pip install -U pip  \
    && pip install poetry

# Create server directories
RUN mkdir -p /nupyserver/log \
    mkdir -p /nupyserver/checkout \
    mkdir -p /nupyserver/packages \
    && chmod -R 777 /nupyserver

# Install server
RUN mkdir /app
COPY ./pyproject.toml /app
COPY ./run.sh /app
COPY ./nupyserver.example.conf /etc/nupyserver.conf

WORKDIR /app
RUN poetry install --no-dev
COPY ./nupyserver /app/nupyserver
RUN poetry install --no-dev
EXPOSE 8080/tcp
ENTRYPOINT /bin/sh /app/run.sh

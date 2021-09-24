# NuPyServer Docker
FROM python:3.7-slim-buster
RUN apt update \
    && apt install git python3-cryptopraphy python3-uvicorn uvicorn -y \
    && pip install -U pip  \
    && pip install fastapi

# Create server directories
RUN mkdir -p /nupyserver/log \
    mkdir -p /nupyserver/checkout \
    mkdir -p /nupyserver/packages \
    && chmod -R 777 /nupyserver

# Install server
RUN mkdir /app
COPY ./run.sh /app
COPY ./nupyserver.example.conf /etc/nupyserver.conf

WORKDIR /app
COPY ./nupyserver /app/nupyserver
EXPOSE 8080/tcp
ENTRYPOINT /bin/sh /app/run.sh

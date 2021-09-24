# NuPyServer Docker
ARG ARCH=arm32v7
FROM ${ARCH}/python:3.7-slim-buster
RUN apt update \
    && apt install git python3-cryptography python3-uvicorn -y \
    && pip3 install fastapi uvicorn aiofiles

# Install server
RUN mkdir -p /app/log
COPY run.sh /app
COPY nupyserver /app/nupyserver

ENV NPS_STORAGE=/nupyserver
ENV NPS_DEV=0
ENV NPS_IP=127.0.0.1

WORKDIR /app
EXPOSE 5000/tcp
ENTRYPOINT /app/run.sh

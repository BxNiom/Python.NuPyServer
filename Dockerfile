# NuPyServer Docker
FROM arm32v7/python:3.7-slim-buster
RUN apt update \
    && apt install git python3-cryptography python3-uvicorn -y \
    && pip3 install fastapi uvicorn

# Create server directories
RUN mkdir -p /nupyserver/log \
    mkdir -p /nupyserver/checkout \
    mkdir -p /nupyserver/packages \
    && chmod -R 777 /nupyserver

# Install server
RUN mkdir /app
COPY ./run.sh /app
COPY ./nupyserver /app/nupyserver
COPY ./nupyserver.example.conf /etc/nupyserver.conf

WORKDIR /app
EXPOSE 8080/tcp
ENTRYPOINT /app/run.sh

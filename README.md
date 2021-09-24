# NuPyServer version 0.2

[![MIT](https://img.shields.io/badge/license-MIT-666666?style=flat-square)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.7-informational?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
<br>[![Docker](https://img.shields.io/badge/docker-2496ed?style=flat-square&logo=docker&logoColor=white)](https://hub.docker.com/u/bxniom)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=flat-square&logo=raspberrypi&logoColor=white)](https://www.raspberrypi.org/)

**Minimalistic NuGet Server running on a Raspberry Pi via Docker**

## Install from DockerHub 

#### Raspberry Pi (ARM)
```shell
sudo docker run --name nupyserver -p 5000:5000 -v /srv/nupyserver:/nupyserver --restart always bxniom/nupyserver:0.2-arm
```

#### amd64
```shell
sudo docker run --name nupyserver -p 5000:5000 -v /srv/nupyserver:/nupyserver --restart always bxniom/nupyserver:0.2-amd
```

## Install from GitHub 

#### Raspberry PI (ARM)
```shell
git clone https://github.com/BxNiom/Python.NuPyServer.git
cd Python.NuPyServer
sudo docker build -t nupyserver:0.2 .
sudo docker run --name nupyserver -p 5000:5000 -v /srv/nupyserver:/nupyserver --restart always nupyserver:0.2  
```

#### amd64
```shell
git clone https://github.com/BxNiom/Python.NuPyServer.git
cd Python.NuPyServer
sudo docker build --build-arg ARCH=amd64 -t nupyserver:0.2 .
sudo docker run --name nupyserver -p 5000:5000 -v /srv/nupyserver:/nupyserver --restart always nupyserver:0.2  
```


## Usage

Add a new NuGet source to your favorite IDE (or command client). The NuPyServer source url is:
```shell
without SSL:
http://[CONTAINER-IP]:[PORT]/v3/index.json

with SSL:
https://[CONTAINER-IP]:[PORT]/v3/index.json
```

Now you can put your NuGet packages (.nupkg) files to the checkout directory in server storage. The server automatically
checkout for new packages every 5 minutes (by default). If you can't wait, just restart the docker container ;)

## Environment variables:

| Name | Default | Description |
-------|---------|-------------|
|NPS_STORAGE | /nupyserver | Storage path in container |
|NPS_CHECKOUT| 5 | Interval in minutes to run checkout
|NPS_SSL_KEY | None | Path to ssl key file in container |
|NPS_SSL_CERT | None | Path to ssl certificate file in container |
|NPS_DEV | 0 | print some extra info's<br>0 = off, 1 = on |

By default, the server runs on port 5000. So be sure you bind this port when creating container.


### Todo

- NuGet protocol version 2

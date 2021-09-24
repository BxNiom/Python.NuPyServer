# NuPyServer version 0.1

Minimalistic NuGet Server running on a Raspberry Pi via Docker

## Install

```
git clone https://github.com/BxNiom/Python.NuPyServer.git
cd Python.NuPyServer
sudo docker build -t arm32v7/nupyserver:py3.7-slim.buster .
sudo docker run --name nupyserver -p 5000:8080 -v /srv/nupyserver:/nupyserver --restart always arm32v7/nupyserver:py3.7-slim.buster  
```

- I am using port 5000 on my network to reach the server
- My storage directory is /srv/nupyserver

## Usage

Just copy your .nupkg files to your server storage checkout directory (e.g. /srv/nupyserver/checkout).
At the moment the interval checkout is not running. So you have to restart the server.

In JetBrains Rider or Visual Studio add your nuget server to the source list:

```shell
http://[Raspberry IP]:[Server Port]/v3/index.json
```

That's it

### Todo

- Checkout
- Better README ;)
- NuGet protocol version 2

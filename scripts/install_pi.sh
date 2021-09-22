#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

echo "Install dependencies..."
apt install build-essential git -y > /dev/null 2>&1
pip3 install poetry > /dev/null 2>&1

echo "Install NuPyServer..."
git clone https://github.com/BxNiom/Python.NuPyServer.git /opt/nupyserver > /dev/null 2>&1
(cd /opt/nupyserver && poetry install --no-dev) > /dev/null 2>&1

echo "Create server storage..."
mkdir /srv/nupyserver > /dev/null 2>&1
mkdir /srv/nupyserver/checkout > /dev/null 2>&1
mkdir /srv/nupyserver/packages > /dev/null 2>&1
mkdir /srv/nupyserver/log > /dev/null 2>&1

echo "Creating configuration..."
echo "[server]" > /etc/nupyserver.conf
echo "host = 127.0.0.1" >> /etc/nupyserver.conf
echo "port = 5050" >> /etc/nupyserver.conf
echo "" >> /etc/nupyserver.conf
echo "# Main storage directory" >> /etc/nupyserver.conf
echo "storage = /srv/nupyserver" >> /etc/nupyserver.conf
echo "# Interval to run check out for new packages" >> /etc/nupyserver.conf
echo "checkout = 5" >> /etc/nupyserver.conf
echo "" >> /etc/nupyserver.conf
echo "# Enable SSL" >> /etc/nupyserver.conf
echo "# ssl_cert = " >> /etc/nupyserver.conf
echo "# ssl_key = " >> /etc/nupyserver.conf
echo "" >> /etc/nupyserver.conf
echo "[protocols] = " >> /etc/nupyserver.conf
echo "version2 = no " >> /etc/nupyserver.conf
echo "version3 = yes" >> /etc/nupyserver.conf

echo "Prepare scripts..."
ln -s /opt/nupyserver/run.sh /usr/bin/nupyserver > /dev/null 2>&1
chmod +x /usr/bin/nupyserver > /dev/null 2>&1

echo "All done."
echo ""
echo "To start server run:            nupyserver"
echo "Configuration file located at:  /etc/nupyserver.conf"
echo "Storage is located at:          /srv/nupyserver"
echo ""
echo "Default URL for the server is:"
echo "   http://localhost:5050"
echo ""
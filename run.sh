#!/bin/bash

echo "     _   _           ____            ____"
echo "    | \ | |  _   _  |  _ \   _   _  / ___|    ___   _ __  __   __   ___   _ __"
echo "    |  \| | | | | | | |_) | | | | | \___ \   / _ \ | '__| \ \ / /  / _ \ | '__|"
echo "    | |\  | | |_| | |  __/  | |_| |  ___) | |  __/ | |     \ V /  |  __/ | |"
echo "    |_| \_|  \__,_| |_|      \__, | |____/   \___| |_|      \_/    \___| |_|"
echo "                             |___/"
echo "                                                                     by BxNiom"
echo ""

# Check directories

if [ ! -d "${NPS_STORAGE}" ]
then
  echo "Create storage directories..."
  mkdir -p "${NPS_STORAGE}/log"
  mkdir -p "${NPS_STORAGE}/checkout"
  mkdir -p "${NPS_STORAGE}/packages"
  chmod -R 777 "${NPS_STORAGE}"
fi

cmd="python3 -m uvicorn nupyserver.server:app --host 0.0.0.0 --port 5000"

if [ ! -z $NPS_SSL_CERT ] && [ ! -z $NPS_SSL_KEY ]
then
    cmd+=" --ssl-keyfile=$NPS_SSL_KEY --ssl-certfile=$NPS_SSL_CERT"
fi

(cd /app && $cmd)

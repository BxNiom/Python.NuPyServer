#!/bin/bash

echo "     _   _           ____            ____"
echo "    | \ | |  _   _  |  _ \   _   _  / ___|    ___   _ __  __   __   ___   _ __"
echo "    |  \| | | | | | | |_) | | | | | \___ \   / _ \ | '__| \ \ / /  / _ \ | '__|"
echo "    | |\  | | |_| | |  __/  | |_| |  ___) | |  __/ | |     \ V /  |  __/ | |"
echo "    |_| \_|  \__,_| |_|      \__, | |____/   \___| |_|      \_/    \___| |_|"
echo "                             |___/"
echo "                                                                     by BxNiom"
echo ""

get_config() { 
    echo $(awk -F "=" "/^$1/ {print \$2}" /etc/nupyserver.conf);
}

host=$(get_config "host")
port=$(get_config "port")
ssl_cert=$(get_config "ssl_cert")
ssl_key=$(get_config "ssl_key")
cmd="python3 -m uvicorn nupyserver.server:app --host $host --port $port"

if [ ! -z $ssl_cert ] && [ ! -z $ssl_key ]
then
    cmd+=" --ssl-keyfile=$ssl_key --ssl-certfile=$ssl_cert"
fi

(cd /app && $cmd)

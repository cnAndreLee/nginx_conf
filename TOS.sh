#!/bin/bash

echo "Input the group A or B"
read group

case $group in
    A)
    port=9001
    ;;

    B)
    port=9002
    ;;

    *)
    echo "Group Error !"
    exit 6
    ;;
esac

echo "Please select tos , Input the 1 or 2"
read tos
case $tos in
    1)
    ;;

    2)
    ;;

    *)
    echo "Input Error!"
    exit 5
    ;;
esac

container_name=TOS_${group}_${tos}

docker stop TOS_${group}_1 TOS_${group}_2
docker rm TOS_${group}_1 TOS_${group}_2


docker run -d --name $container_name --restart=always -p 0.0.0.0:$port:$port/tcp -v /root/nginx_conf/TOS/TOS_${group}_${tos}.conf:/etc/nginx/nginx.conf:ro nginx:latest

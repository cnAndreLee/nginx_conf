#!/bin/bash

echo "Input the red or green"
read xcc

case $xcc in
    red)
    port=8003
    ;;

    green)
    port=8004
    ;;

    *)
    echo "Input Error!"
    exit 5
    ;;
esac

echo "Input the group A or B"
read group

case $group in
    A)
    ;;
    B)
    ;;
    *)
    echo "Group Error !"
    exit 6
    ;;
esac

container_name=XCC_${xcc}_${group}

docker stop XCC_${xcc}_A XCC_${xcc}_B
docker rm XCC_${xcc}_A XCC_${xcc}_B


docker run -d --name $container_name --restart=always -p 0.0.0.0:$port:$port/tcp -v /root/nginx_conf/XCC/XCC_${xcc}_${group}.conf:/etc/nginx/nginx.conf:ro nginx:latest

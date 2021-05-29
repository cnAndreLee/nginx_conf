#!/bin/bash

echo "Input the Car ID"
read car

case $car in
    A011)
    port=7011
    ;;

    A031)
    port=7031
    ;;

    A032)
    port=7032
    ;;

    *)
    echo "Car ID Error!"
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

container_name=ACT_${car}_${group}

docker stop ACT_${car}_A ACT_${car}_B
docker rm ACT_${car}_A ACT_${car}_B

docker run -d --name $container_name --restart=always -p 0.0.0.0:$port:$port/tcp -v /root/nginx_conf/ACT/ACT_${car}_${group}.conf:/etc/nginx/nginx.conf:ro nginx:latest

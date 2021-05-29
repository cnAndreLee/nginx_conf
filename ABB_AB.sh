docker stop ABB_AB

docker rm ABB_AB

docker run -d --name ABB_AB -p 0.0.0.0:80:80/tcp -v /root/nginx_conf/ABB_AB.conf:/etc/nginx/nginx.conf:ro nginx:latest

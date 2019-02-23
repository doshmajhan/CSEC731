FROM ubuntu:latest

RUN apt update
RUN apt install -y apache2 php
ADD /tmp/docker/vuln.php /var/www/html/vuln.php
EXPOSE 80 443
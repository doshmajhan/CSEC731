FROM ubuntu:latest

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update
RUN apt install -y apache2 php libapache2-mod-php

COPY docker-entrypoint.sh /
COPY vuln.php /var/www/html/vuln.php
COPY server.crt /etc/apache2/ssl/server.crt
COPY server.key /etc/apache2/ssl/server.key
COPY dev.conf /etc/apache2/sites-enabled/dev.conf

RUN a2enmod ssl
RUN service apache2 restart
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["apachectl", "-D", "FOREGROUND"]
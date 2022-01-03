FROM sarlos/python:3.9

RUN apt-get update \
 && apt-get install -y nginx \
 && apt-get clean
RUN pip3 install flack flask-cors pillow uwsgi

RUN mkdir /var/www/icon-maker
COPY ui/dist /var/www/icon-maker/
COPY misc/default.conf /etc/nginx/conf.d/

WORKDIR /app
COPY src ./
COPY misc/app.ini ./

VOLUME /app/static

COPY misc/entrypoint.sh /
ENTRYPOINT /entrypoint.sh

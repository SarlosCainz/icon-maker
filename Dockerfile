FROM sarlos/python:3.9-im

RUN apt-get update \
 && apt-get install -y nginx \
 && apt-get clean
RUN pip3 install flack flask-cors pillow Wand fasttext-langdetect wget uwsgi

RUN mkdir /var/www/icon-maker
COPY ui/dist /var/www/icon-maker/
COPY misc/nginx.conf /etc/nginx/

WORKDIR /app
COPY src ./
COPY misc/app.ini ./
COPY misc/manifest.webmanifest ./
COPY misc/sample.html ./

VOLUME /app/static
EXPOSE 80

RUN set -eux \
 && rm -r /var/log/nginx/*.log \
 && ln -s /dev/stdout /var/log/nginx/access.log \
 && ln -s /dev/stderr /var/log/nginx/error.log

COPY misc/entrypoint.sh /
ENTRYPOINT /entrypoint.sh

FROM python:3.11

RUN --mount=type=cache,target=/var/lib/apt,sharing=locked \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update && apt-get install -y nginx

RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

WORKDIR /var/www/icon-maker
COPY ui/dist ./
COPY misc/nginx.conf /etc/nginx/

WORKDIR /app
# フォントは変更が少ないため、変更の多いファイルより前に置いてレイヤーを再利用する
COPY misc/fonts ./fonts
COPY src ./
COPY misc/app.ini ./
COPY misc/manifest.webmanifest ./
COPY misc/sample.html ./

EXPOSE 80

RUN set -eux \
 && rm -r /var/log/nginx/*.log \
 && ln -s /dev/stdout /var/log/nginx/access.log \
 && ln -s /dev/stderr /var/log/nginx/error.log

COPY misc/entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

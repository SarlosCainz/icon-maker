#!/bin/bash

set -eu

trap 'kill $(jobs -p)' INT TERM

nginx &
uwsgi --ini /app/app.ini &

wait

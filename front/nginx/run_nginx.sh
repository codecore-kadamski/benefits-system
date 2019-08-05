#!/usr/bin/env bash
export DOLLAR='$'
envsubst < /etc/nginx/default.conf.template > /etc/nginx/nginx.conf
nginx -g "daemon off;"


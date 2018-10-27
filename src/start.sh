#!/bin/sh

python stop_proxies.py

/usr/local/bin/gunicorn -b :$1 app:app
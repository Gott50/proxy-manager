#!/bin/sh

python setup.py

/usr/local/bin/gunicorn -b :$1 app:app
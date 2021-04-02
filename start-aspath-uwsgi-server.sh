#!/usr/bin/env bash

if [[ -e venv/bin/activate ]]; then
    echo "activating virtualenv"
    source venv/bin/activate
fi

uwsgi --http 0.0.0.0:8080 --wsgi-file app.py --callable app --master --processes 4 --threads 2 --safe-pidfile /tmp/aspath-uwsgi-server.pid

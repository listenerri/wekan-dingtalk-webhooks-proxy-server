#!/usr/bin/env bash

if [[ -e venv/bin/activate ]]; then
    echo "activating virtualenv"
    source venv/bin/activate
fi

if [[ -e /tmp/aspath-uwsgi-server.pid ]]; then
    uwsgi --stop /tmp/aspath-uwsgi-server.pid
else
    echo "Error: not find uwsgi pid file"
    exit 255
fi

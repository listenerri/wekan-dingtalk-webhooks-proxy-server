#!/usr/bin/env bash

set -e

if [[ -z $(which pip3) ]]; then
    echo "Error: require pip3"
    exit 255
fi

if [[ -z $(which virtualenv) ]]; then
    pip3 install virtualenv
fi

virtualenv -p python3 venv
source venv/bin/activate

# uwsgi require
sudo apt-get install libpcre3 libpcre3-dev

pip3 install -r ./requirements.txt

echo "Note: run the following command to enter virtualenv:"
echo "source venv/bin/activate"

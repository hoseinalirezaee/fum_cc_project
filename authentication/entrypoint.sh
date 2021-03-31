#!/bin/bash

set -e

python3 main/wait_script.py

python3 manage.py migrate --no-input
python3 manage.py loaddata fakedata.json
gunicorn -b 0.0.0.0:8000 main.wsgi:application

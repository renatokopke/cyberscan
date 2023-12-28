#!/usr/bin/env bash
set -ueo pipefail;

apt-get update -y
apt-get install -y build-essential

cd /app
pip3 install mysqlclient
pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

python manage.py makemigrations
python manage.py migrate

# --link    Create a symbolic link to each file instead of copying.
# --noinput Do NOT prompt the user for input of any kind.
#
python manage.py collectstatic -link --noinput

python manage.py runserver 0.0.0.0:8000
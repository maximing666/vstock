#!/bin/bash
apt-get update && apt-get install -y telnet
cd /opt/conda/vstock/ && conda install --file requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:18001
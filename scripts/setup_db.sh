#! /usr/bin/bash

psql -U postgres -c "DROP DATABASE lcai"
psql -U postgres -c "CREATE DATABASE lcai"
python manage.py migrate
python manage.py createcachetable
python manage.py packages -o load_package -s pkg --yes

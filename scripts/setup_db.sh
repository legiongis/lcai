#! /usr/bin/bash

psql -U postgres -c "DROP DATABASE lcai WITH (FORCE)"
psql -U postgres -c "CREATE DATABASE lcai"

python manage.py es delete_indexes
python manage.py es setup_indexes
python manage.py migrate
python manage.py createcachetable

python manage.py packages -o import_graphs -s lcai/system_settings/Arches_System_Settings_Model.json
python manage.py packages -o import_business_data -s lcai/system_settings/System_Settings.json -ow overwrite

python manage.py packages -o load_package -s pkg
python manage.py fixbasemaps

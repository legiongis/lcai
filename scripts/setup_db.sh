#! /usr/bin/bash

psql -U postgres -h localhost -c "DROP DATABASE lcai WITH (FORCE)"
psql -U postgres -h localhost -c "CREATE DATABASE lcai"

uv run manage.py es delete_indexes
uv run manage.py es setup_indexes
uv run manage.py migrate
uv run manage.py createcachetable

uv run manage.py packages -o import_graphs -s lcai/system_settings/Arches_System_Settings_Model.json
uv run manage.py packages -o import_business_data -s lcai/system_settings/System_Settings.json -ow overwrite

uv run manage.py packages -o load_package -s pkg
uv run manage.py fixbasemaps

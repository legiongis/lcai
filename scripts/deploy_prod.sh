#! /usr/bin/bash

npm run build_development

uv run manage.py collectstatic --noinput

touch lcai/wsgi.py

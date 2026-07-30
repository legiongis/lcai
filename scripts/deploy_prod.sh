#! /usr/bin/bash


#rm static_root -r
npm run build_development

uv run manage.py collectstatic --noinput

touch lcai/wsgi.py

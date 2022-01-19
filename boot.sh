#!/bin/bash
export FLASK_APP=api.py
flask db upgrade

exec gunicorn -b :5000 api:app &
exec python worker.py
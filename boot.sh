#!/bin/bash

sleep 2
flask db upgrade
exec gunicorn -b :5000 --workers=6 --access-logfile - --error-logfile - pushup-tracker:app

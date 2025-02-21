#!/bin/sh

# Collect static files
python manage.py collectstatic --noinput

# Pause so databases can start properly
sleep 1m

# Adding enviroment variables into system
printenv | grep -v "no_proxy" >> /etc/environment

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Crons for text parsing and autotagging
service cron start

# Service start
python manage.py start_bot_telegram > /app/log_bot.log 2>&1 &
python manage.py runserver 0.0.0.0:8000
